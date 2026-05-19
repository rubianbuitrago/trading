# analysis/performance_dashboard.py
"""
Dashboard de rendimiento offline para backtesting de estrategias de scalping.
Analiza todas las estrategias largas en datos históricos y genera reportes HTML.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
from datetime import timedelta
import os
import sys
import warnings
from pathlib import Path
import json

warnings.filterwarnings('ignore')

# ================= IMPORTACIONES COMPATIBLES =================
import yfinance as yf
from datetime import datetime

# Importar desde core
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.indicators import calculate_indicators
from core.market_regime import compute_regime
from core.signals.registry import calculate_all_signals, get_signal_by_column, get_long_column_names

# ================= CONFIGURACIÓN =================
SYMBOL = "NVDA"
DATA_SOURCE = "CSV"            # "Yahoo" o "CSV"
PERIOD = "5d"                    # Solo para Yahoo
INTERVAL = "1m"
INITIAL_CAPITAL = 1000
COOLDOWN_MINUTES = 60
COMMISSION = 0.0
MIN_CONSENSO = 1

# ================= FUNCIONES DE CARGA MEJORADAS =================

def load_csv_data(filepath):
    """Carga datos desde un archivo CSV con formato estándar."""
    try:
        df = pd.read_csv(filepath)
        expected_cols = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Verificar si existen todas las columnas necesarias
        if not all(col in df.columns for col in expected_cols):
            print(f"⚠️ Columnas disponibles: {df.columns.tolist()}")
            missing = set(expected_cols) - set(df.columns)
            print(f"❌ Columnas faltantes: {missing}")
            return pd.DataFrame()
        
        df = df[expected_cols]
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'])
        df = df[df['Volume'] > 0]  # Filtrar volumen cero
        df = df.sort_values('Datetime').reset_index(drop=True)
        
        print(f"✅ CSV cargado exitosamente: {len(df)} filas")
        return df
    
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")
        return pd.DataFrame()


def load_yahoo_data_robust(symbol, period="5d", interval="1m"):
    """Carga datos de Yahoo Finance con manejo robusto de errores."""
    try:
        print(f"📥 Descargando {symbol} desde Yahoo Finance ({period})...")
        data = yf.download(symbol, period=period, interval=interval, progress=False)
        
        if data.empty:
            print(f"❌ Yahoo retornó datos vacíos")
            return pd.DataFrame()
        
        # Aplanar multiíndice si existe
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        data = data.reset_index()
        if 'Date' in data.columns:
            data.rename(columns={'Date': 'Datetime'}, inplace=True)
        elif 'Datetime' not in data.columns:
            data.rename(columns={data.columns[0]: 'Datetime'}, inplace=True)
        
        # Seleccionar columnas esperadas
        expected_cols = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
        available = [col for col in expected_cols if col in data.columns]
        data = data[available]
        
        # Convertir a datetime
        data['Datetime'] = pd.to_datetime(data['Datetime'])
        
        # Eliminar zona horaria si existe
        if data['Datetime'].dt.tz is not None:
            data['Datetime'] = data['Datetime'].dt.tz_localize(None)
        
        # Convertir a numérico
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        data = data.dropna(subset=['Close'])
        data = data.sort_values('Datetime').reset_index(drop=True)
        
        print(f"✅ Datos de Yahoo cargados: {len(data)} filas")
        return data
    
    except Exception as e:
        print(f"❌ Error descargando de Yahoo: {e}")
        return pd.DataFrame()


def get_csv_path_from_user():
    """Obtiene la ruta del CSV desde argumento o input interactivo."""
    if len(sys.argv) > 1:
        ruta = Path(sys.argv[1])
        if ruta.exists():
            print(f"✅ Usando archivo desde argumento: {ruta}")
            return ruta
        else:
            print(f"⚠️ Archivo del argumento no existe: {ruta}")
    
    print("\n📁 Proporciona la ruta del archivo CSV con datos históricos.")
    print("   (Puedes arrastrar el archivo hasta la terminal)")
    entrada = input("Ruta CSV (deja vacío para usar Yahoo Finance): ").strip().strip('"')
    
    if not entrada:
        print("→ Se usará Yahoo Finance")
        return None
    
    ruta = Path(entrada)
    if not ruta.exists():
        print(f"❌ Archivo no existe: {ruta}")
        return None
    
    return ruta


def load_data():
    """Carga datos según configuración o entrada del usuario."""
    if DATA_SOURCE == "CSV":
        csv_path = get_csv_path_from_user()
        if csv_path is None:
            print("→ Fallback a Yahoo Finance")
            return load_yahoo_data_robust(SYMBOL, period=PERIOD, interval=INTERVAL)
        else:
            return load_csv_data(csv_path)
    else:
        return load_yahoo_data_robust(SYMBOL, period=PERIOD, interval=INTERVAL)


# ================= FUNCIONES DE BACKTESTING =================

def simulate_strategy(df, signal_col, initial_capital, cooldown_minutes, commission, min_consenso=1):
    """
    Simula operaciones largas para una estrategia individual.
    Usa tp_mult y sl_mult de cada clase de estrategia.
    """
    capital = initial_capital
    equity = [capital]
    trades = []
    
    in_trade = False
    entry_price = entry_time = stop_loss = take_profit = entry_strategy = None
    last_close_time = None
    
    try:
        strat_obj = get_signal_by_column(signal_col)
        tp_mult = strat_obj.tp_mult
        sl_mult = strat_obj.sl_mult
    except Exception as e:
        print(f"⚠️ No se pudo obtener estrategia {signal_col}: {e}")
        tp_mult = 1.5
        sl_mult = 0.5
    
    for i in range(len(df)):
        if signal_col not in df.columns:
            equity.append(capital)
            continue
        
        current_price = df['Close'].iloc[i]
        current_time = df['Datetime'].iloc[i]
        atr = df['ATR14'].iloc[i] if 'ATR14' in df.columns and not pd.isna(df['ATR14'].iloc[i]) else 0.2
        
        if in_trade:
            # Trailing stop
            if current_price > entry_price:
                new_stop = current_price - sl_mult * atr
                if new_stop > stop_loss:
                    stop_loss = new_stop
            
            # Verificar cierre
            exit_price = None
            if current_price <= stop_loss:
                exit_price = stop_loss
            elif current_price >= take_profit:
                exit_price = take_profit
            
            if exit_price is not None:
                ret_pct = (exit_price / entry_price - 1) * 100
                capital *= (1 + ret_pct / 100 - commission / 100)
                trades.append({
                    'entry_time': entry_time,
                    'exit_time': current_time,
                    'return_pct': ret_pct,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'side': 'long',
                    'strategy': signal_col,
                    'commission': commission
                })
                in_trade = False
        else:
            # Sin operación abierta: buscar entrada
            if cooldown_minutes > 0 and last_close_time is not None:
                if current_time - last_close_time < timedelta(minutes=cooldown_minutes):
                    equity.append(capital)
                    continue
            
            # Señal activa
            if df[signal_col].iloc[i]:
                entry_price = current_price
                entry_time = current_time
                entry_strategy = signal_col
                stop_loss = entry_price - sl_mult * atr
                take_profit = entry_price + tp_mult * atr
                in_trade = True
                last_close_time = None
        
        equity.append(capital)
    
    # Cerrar operación abierta al final
    if in_trade and len(trades) < len(equity):
        last_price = df['Close'].iloc[-1]
        ret_pct = (last_price / entry_price - 1) * 100
        capital *= (1 + ret_pct / 100)
        trades.append({
            'entry_time': entry_time,
            'exit_time': df['Datetime'].iloc[-1],
            'return_pct': ret_pct,
            'entry_price': entry_price,
            'exit_price': last_price,
            'side': 'long',
            'strategy': signal_col,
            'commission': commission
        })
        equity.append(capital)
    
    return trades, equity


def compute_metrics(trades, equity, initial_capital):
    """Calcula métricas de rendimiento."""
    if not trades:
        return {
            'total_trades': 0,
            'win_rate': 0,
            'total_return': 0,
            'profit_factor': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'avg_win': 0,
            'avg_loss': 0
        }
    
    df_t = pd.DataFrame(trades)
    wins = df_t[df_t['return_pct'] > 0]
    losses = df_t[df_t['return_pct'] < 0]
    
    n = len(df_t)
    win_rate = (len(wins) / n * 100) if n > 0 else 0
    total_return = (equity[-1] - initial_capital) / initial_capital * 100 if initial_capital > 0 else 0
    
    profit_factor = 0
    if len(losses) > 0 and losses['return_pct'].sum() != 0:
        profit_factor = wins['return_pct'].sum() / abs(losses['return_pct'].sum())
    
    # Max drawdown
    peak = equity[0]
    max_dd = 0
    for v in equity:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100 if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
    
    # Sharpe ratio
    df_t['date'] = pd.to_datetime(df_t['exit_time']).dt.date
    daily = df_t.groupby('date')['return_pct'].sum()
    sharpe = 0
    if len(daily) > 1 and daily.std() > 0:
        sharpe = daily.mean() / daily.std() * np.sqrt(252)
    
    avg_win = wins['return_pct'].mean() if len(wins) > 0 else 0
    avg_loss = losses['return_pct'].mean() if len(losses) > 0 else 0
    
    return {
        'total_trades': n,
        'win_rate': round(win_rate, 1),
        'total_return': round(total_return, 2),
        'profit_factor': round(profit_factor, 2),
        'max_drawdown': round(max_dd, 2),
        'sharpe_ratio': round(sharpe, 2),
        'avg_win': round(avg_win, 2),
        'avg_loss': round(avg_loss, 2)
    }


# ================= VISUALIZACIONES =================

def create_equity_chart(trades, equity, initial_capital, title="Equity Curve"):
    """Crea gráfico de curva de capital."""
    fig = go.Figure()
    
    # Línea de equity
    fig.add_trace(go.Scatter(
        y=equity,
        mode='lines',
        name='Equity',
        line=dict(color='green', width=2)
    ))
    
    # Línea de capital inicial
    fig.add_hline(y=initial_capital, line_dash="dash", line_color="gray", 
                  annotation_text="Capital inicial")
    
    fig.update_layout(
        title=title,
        xaxis_title="Operación",
        yaxis_title="Capital (USD)",
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_metrics_table(strategies_metrics):
    """Crea tabla de métricas por estrategia."""
    df = pd.DataFrame(strategies_metrics).T
    df = df.sort_values('total_return', ascending=False)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Estrategia'] + list(df.columns),
            fill_color='paleturquoise',
            align='left',
            font=dict(size=12)
        ),
        cells=dict(
            values=[df.index.tolist()] + [df[col].tolist() for col in df.columns],
            fill_color='lavender',
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title="Métricas por estrategia",
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


# ================= MAIN =================

def main():
    """Ejecuta el análisis completo."""
    
    print("\n" + "="*80)
    print("📊 DASHBOARD DE RENDIMIENTO - BACKTEST DE ESTRATEGIAS DE SCALPING")
    print("="*80 + "\n")
    
    # 1. Cargar datos
    df = load_data()
    if df.empty:
        print("❌ No se pudieron cargar datos. Abortando.")
        return
    
    print(f"\n📈 Datos cargados: {len(df)} velas | Rango: {df['Datetime'].min()} a {df['Datetime'].max()}")
    
    # 2. Calcular indicadores
    print("\n⚙️ Calculando indicadores...")
    df = calculate_indicators(df)
    df = compute_regime(df)
    df = calculate_all_signals(df)
    print("✅ Indicadores calculados")
    
    # 3. Obtener estrategias largas
    all_long_cols = get_long_column_names()
    print(f"\n📋 Estrategias largas encontradas: {len(all_long_cols)}")
    for col in all_long_cols:
        print(f"   • {col}")
    
    # 4. Evaluación individual
    print("\n" + "="*80)
    print("🔍 EVALUACIÓN INDIVIDUAL DE ESTRATEGIAS")
    print("="*80 + "\n")
    
    individual_results = {}
    for col in all_long_cols:
        print(f"Analizando {col}...", end=" ")
        trades, equity = simulate_strategy(df, col, INITIAL_CAPITAL, COOLDOWN_MINUTES, COMMISSION)
        metrics = compute_metrics(trades, equity, INITIAL_CAPITAL)
        individual_results[col] = {'trades': trades, 'equity': equity, 'metrics': metrics}
        print(f"✓ ({metrics['total_trades']} op, {metrics['win_rate']}% WR, {metrics['total_return']:+.2f}%)")
    
    # 5. Mostrar tabla de resultados
    print("\n" + "-"*80)
    df_results = pd.DataFrame({col: metrics['metrics'] for col, metrics in individual_results.items()}).T
    df_results = df_results.sort_values('total_return', ascending=False)
    print(df_results.to_string())
    
    # 6. Seleccionar mejores estrategias
    print("\n" + "="*80)
    print("🏆 SELECCIÓN DE MEJORES ESTRATEGIAS")
    print("="*80 + "\n")
    
    selected_cols = [
        col for col, data in individual_results.items()
        if data['metrics']['win_rate'] >= 45 and data['metrics']['total_return'] > 0
    ]
    
    if not selected_cols:
        print("⚠️ No se encontraron estrategias rentables. Usando las 3 mejores por ROI...")
        selected_cols = df_results.head(3).index.tolist()
    
    print(f"✅ Estrategias seleccionadas ({len(selected_cols)}):")
    for col in selected_cols:
        metrics = individual_results[col]['metrics']
        print(f"   • {col}")
        print(f"     └─ {metrics['total_trades']} op | {metrics['win_rate']}% WR | {metrics['total_return']:+.2f}% ROI")
    
    # 7. Generar reportes HTML
    print("\n" + "="*80)
    print("📊 GENERANDO REPORTES HTML")
    print("="*80 + "\n")
    
    # Gráficos individuales para las 3 mejores
    for i, col in enumerate(df_results.head(3).index):
        if col in individual_results:
            equity = individual_results[col]['equity']
            fig = create_equity_chart(
                individual_results[col]['trades'],
                equity,
                INITIAL_CAPITAL,
                title=f"Equity - {col}"
            )
            filename = f"equity_{col}_{i+1}.html"
            fig.write_html(filename)
            print(f"✅ {filename}")
    
    # Tabla comparativa
    fig_metrics = create_metrics_table(
        {col: individual_results[col]['metrics'] for col in individual_results}
    )
    fig_metrics.write_html("estrategias_metricas.html")
    print("✅ estrategias_metricas.html")
    
    # Gráfico de barras de ROI
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Bar(
        x=df_results.index,
        y=df_results['total_return'],
        marker=dict(color=df_results['total_return'], colorscale='RdYlGn', 
                    cmid=0, showscale=True),
        text=df_results['total_return'].round(1),
        textposition='auto',
    ))
    fig_roi.update_layout(
        title="ROI por estrategia",
        xaxis_title="Estrategia",
        yaxis_title="ROI (%)",
        height=500,
        template="plotly_white"
    )
    fig_roi.write_html("rentabilidad_barras.html")
    print("✅ rentabilidad_barras.html")
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN FINAL")
    print("="*80)
    print(f"Capital inicial: ${INITIAL_CAPITAL:.2f}")
    print(f"Total operaciones: {sum(data['metrics']['total_trades'] for data in individual_results.values())}")
    print(f"Mejor estrategia: {df_results.index[0]} ({df_results['total_return'].iloc[0]:+.2f}%)")
    print(f"Peor estrategia: {df_results.index[-1]} ({df_results['total_return'].iloc[-1]:+.2f}%)")
    print(f"\n✅ Reportes generados en: {os.getcwd()}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
