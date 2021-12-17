# env_PaceRaceV2 
ist überarbeitet und enthält bereits die Implementierung für die akutelle Version (auskommentiert) von gym. Diese ist über anaconda noch nicht verfügbar.
Die Überabeitung basiert auf https://github.com/openai/gym/blob/master/gym/envs/classic_control/continuous_mountain_car.py und sollte daher der BEST-PRACTISE entsprechen.

# ToDo:
- Fehler von Observation space und return von reset() -> siehe check env
- Streckenbegrenzung / Kollisionsabfrage + Aufnahme in Reward-Function + ggf. reset
- Reward nach Streckenabschnitten

yaw angle

sin(yaw_angle)
cos(yaw_angle)

359° 1°

