# config/variables.py
"""
Parámetros centralizados de todas las estrategias largas y cortas.
Aquí se definen los valores por defecto. Los cambios se aplican automáticamente.
"""

STRATEGY_PARAMS = {
    # ==================== ESTRATEGIAS LARGAS EXISTENTES ====================
    "RSIVolLong": {
        "tp_mult": 2.5,
        "sl_mult": 0.5,
        "rsi_threshold": 32,
        "vol_threshold": 1.4,
        "min_periods": 20,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "EMACrossLong": {
        "tp_mult": 2.5,
        "sl_mult": 0.5,
        "vol_threshold": 1.2,
        "ema_fast": 9,
        "ema_slow": 20,
        "use_sma200": True,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "PullbackSMA20Long": {
        "tp_mult": 1.0,
        "sl_mult": 0.5,
        "vol_threshold": 1.8,
        "sma_tendencia_period": 10,
        "tol_sma": 0.004,
        "rsi_max": 45,
        "use_sma200": True,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },
    "RangeBreakLong": {
        "tp_mult": 2.5,
        "sl_mult": 0.5,
        "range_window": 15,
        "vol_threshold": 2.2,
        "range_size_max": 0.004,
        "atr_mult_break": 1.3,
        "trailing_activation_pct": 0.6,
        "trailing_distance_mult": 1.2,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.4
    },
    "PSARVolLong": {
        "tp_mult": 1.2,
        "sl_mult": 0.5,
        "vol_threshold": 2.0,
        "adx_threshold": 20,
        "use_sma200": True,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },
    "PullbackEMA9Long": {
        "tp_mult": 0.8,
        "sl_mult": 0.4,
        "vol_threshold": 1.5,
        "tol_ema": 0.002,
        "ema_fast": 9,
        "ema_slow": 20,
        "use_sma200": False,
        "trailing_activation_pct": 0.3,
        "trailing_distance_mult": 0.6,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },
    "StochRSIATRLong": {
        "tp_mult": 1.5,
        "sl_mult": 0.6,
        "stoch_k_threshold": 30,
        "atr_mult_price": 0.0012,
        "vol_threshold": 1.5,
        "use_sma200": True,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "LiquidityGrabLong": {
        "tp_mult": 1.2,
        "sl_mult": 0.6,
        "low_window": 5,
        "vol_threshold": 2.0,
        "use_sma200": True,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },
    "SupportTouchLong": {
        "tp_mult": 2.0,
        "sl_mult": 0.5,
        "low_window": 15,
        "zone_tol": 0.0015,
        "rsi_max": 38,
        "vol_threshold": 1.3,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "TrendChangeLong": {
        "tp_mult": 2.5,
        "sl_mult": 0.6,
        "rsi_max": 40,
        "vol_threshold": 1.5,
        "low_window": 10,
        "soporte_tol": 0.008,
        "trailing_activation_pct": 0.6,
        "trailing_distance_mult": 1.2,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.4
    },
    "EMARibbonLong": {
        "tp_mult": 1.0,
        "sl_mult": 0.4,
        "vol_threshold": 2.0,
        "ema_periods": [10, 20, 50, 100],
        "use_sma200": True,
        "adx_threshold": 20,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },
    "BollingerBounceLong": {
        "tp_mult": 2.5,
        "sl_mult": 0.5,
        "vol_threshold": 1.5,
        "rsi_max": 40,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "MACDEMALong": {
        "tp_mult": 1.2,
        "sl_mult": 0.5,
        "macd_threshold": 0.5,
        "vol_threshold": 2.0,
        "use_sma200": True,
        "adx_threshold": 20,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },
    "ReversalNVDA": {
        "tp_mult": 2.5,
        "sl_mult": 0.6,
        "rsi_os": 30,
        "stoch_os": 20,
        "anchura_atr_mult": 1.5,
        "ventana_soporte": 15,
        "tol_ema": 0.02,
        "num_soportes": 3,
        "ema_fast": 45,
        "usar_filtro_horario": True,
        "hora_inicio": 9,
        "hora_fin": 16,
        "usar_rsi5_refuerzo": True,
        "rsi5_os": 35,
        "trailing_activation_pct": 0.5,
        "trailing_distance_mult": 1.0,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.3
    },

    # ==================== NUEVA ESTRATEGIA: PULLBACK SMA200 LARGO ====================
    "PullbackSMA200Long": {
        "tp_mult": 2.0,
        "sl_mult": 0.6,
        "tol_interest": 0.005,
        "tol_trigger": 0.001,
        "use_dynamic_tol": True,
        "atr_tol_factor": 0.5,
        "vol_threshold": 1.2,
        "require_bullish_candle": True,
        "use_rsi5_filter": True,
        "rsi5_threshold": 40,
        "use_stoch": True,
        "stoch_threshold": 25,
        "use_bos": False,
        "use_ema_trailing": False,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },

    # ==================== NUEVA ESTRATEGIA: PULLBACK SMA200 CORTO ====================
    "PullbackSMA200Short": {
        "tp_mult": 2.0,
        "sl_mult": 0.6,
        "tol_interest": 0.005,
        "tol_trigger": 0.001,
        "use_dynamic_tol": True,
        "atr_tol_factor": 0.5,
        "vol_threshold": 1.2,
        "require_bearish_candle": True,
        "use_rsi5_filter": True,
        "rsi5_threshold": 60,
        "use_stoch": True,
        "stoch_threshold": 75,
        "use_bos": False,
        "use_ema_trailing": False,
        "trailing_activation_pct": 0.4,
        "trailing_distance_mult": 0.8,
        "use_atr_for_trailing": True,
        "breakeven_activation_pct": 0.2
    },

    # ==================== PARÁMETROS DE LÍNEAS DE TENDENCIA ====================
    "TrendlineBreak": {
        "vol_threshold": 1.2,
        "atr_tolerance": 0.2,
        "validity_minutes": 45,
        "require_candle_strength": True,
        "min_candle_body_ratio": 0.6,
        "use_trend_filter": False,
        "trend_ema_period": 20,
        "pre_break_alert": True,
        "require_volume_surge": True,
        "volume_surge_window": 3,
        "volume_surge_mult": 1.5,
        "retest_entry": False,
    }
}

# ==================== PARÁMETROS ADICIONALES PARA RUPTURAS DE LÍNEAS DE TENDENCIA ====================
# Estos se usan en core/signal_processor.py en detect_trendline_break_enhanced()
TRENDLINE_BREAK_PARAMS = {
    "vol_rel_threshold": 1.2,              # Volumen relativo mínimo para confirmar ruptura
    "atr_tolerance": 0.2,                  # Tolerancia en múltiplos de ATR
    "validity_minutes": 45,                # Minutos que la línea es válida desde el segundo punto
    "require_candle_strength": True,       # Exigir vela con cuerpo fuerte (> 60% del rango)
    "min_candle_body_ratio": 0.6,          # Ratio mínimo cuerpo/rango de la vela
    "require_volume_surge": True,          # Exigir volumen acumulado en últimas velas
    "volume_surge_window": 3,              # Ventana de velas para volumen acumulado
    "volume_surge_mult": 1.5,              # Multiplicador sobre media móvil de volumen
    "min_distance_atr": 0.5,               # Distancia mínima en ATR para ruptura fuerte
    "use_trend_filter": False,             # Filtrar por régimen (bullish/bearish)
    "adx_threshold": 20,                   # ADX mínimo para considerar tendencia válida
}

# ==================== PARÁMETROS PARA EVALUACIÓN DE LÍNEAS DE TENDENCIA ====================
# Estos se usan en core/trendlines/evaluation.py
TRENDLINE_EVALUATION_PARAMS = {
    "vol_threshold": 1.2,
    "atr_tolerance": 0.2,
    "validity_minutes": 45,
    "require_candle_strength": True,
    "min_candle_body_ratio": 0.6,
    "require_volume_surge": True,
    "volume_surge_window": 3,
    "volume_surge_mult": 1.5,
}
