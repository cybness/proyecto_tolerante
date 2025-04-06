# Sistema distribuido de respaldo tolerante a fallos

## Descripción

Este sistema permite que múltiples nodos hagan respaldo automático de sus archivos entre sí. Si uno falla, otro puede restaurarlo.

## Estructura

- `node.py`: servidor HTTP que recibe respaldos
- `watcher.py`: detecta cambios locales y los envía a vecinos
- `monitor.py`: detecta caídas y restaura archivos desde backup
- `my_files/`: archivos importantes del nodo
- `backups/`: backups recibidos de otros nodos
- `restored_nodes/`: restauraciones realizadas en caso de fallo
