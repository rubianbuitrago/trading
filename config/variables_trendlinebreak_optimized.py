# config/variables_trendlinebreak_optimized.py
"""
Parámetros optimizados para TrendlineBreak.
Prueba estos valores para activar más alarmas sin ser demasiado agresivo.
"""

# OPCIÓN 1: Más permisivo (comienza aquí)
TRENDLINEBREAK_OPTIMIZED_V1 = {
    "vol_threshold": 0.9,              # Reducido de 1.2
    "atr_tolerance": 0.15,             # Reducido de 0.2
    "validity_minutes": 45,
    "require_candle_strength": False,  # DESACTIVADO - crítico
    "min_candle_body_ratio": 0.5,      # Reducido de 0.6
    "use_trend_filter": False,
    "trend_ema_period": 20,
    "pre_break_alert": True,
    "require_volume_surge": False,     # DESACTIVADO - crítico
    "volume_surge_window": 3,
    "volume_surge_mult": 1.2,          # N/A si require_volume_surge=False
    "retest_entry": False,
}

# OPCIÓN 2: Muy permisivo (si V1 sigue sin alarmas)
TRENDLINEBREAK_OPTIMIZED_V2 = {
    "vol_threshold": 0.75,             # Muy bajo
    "atr_tolerance": 0.10,             # Muy bajo
    "validity_minutes": 45,
    "require_candle_strength": False,
    "min_candle_body_ratio": 0.3,
    "use_trend_filter": False,
    "trend_ema_period": 20,
    "pre_break_alert": True,
    "require_volume_surge": False,
    "volume_surge_window": 3,
    "volume_surge_mult": 1.0,
    "retest_entry": False,
}

# OPCIÓN 3: Equilibrio (mejor balance señal/ruido)
TRENDLINEBREAK_OPTIMIZED_V3 = {
    "vol_threshold": 1.0,              # Neutral
    "atr_tolerance": 0.12,             # Moderado
    "validity_minutes": 45,
    "require_candle_strength": False,
    "min_candle_body_ratio": 0.45,
    "use_trend_filter": False,
    "trend_ema_period": 20,
    "pre_break_alert": True,
    "require_volume_surge": True,      # Pero con multiplicador bajo
    "volume_surge_window": 2,
    "volume_surge_mult": 0.9,          # Muy bajo = casi siempre se cumple
    "retest_entry": False,
}

# RECOMENDACIÓN: Comienza con V1, si no hay alarmas pasa a V2
# Después de obtener alarmas, ajusta manualmente si necesitas menos ruido
