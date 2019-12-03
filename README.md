# SnowflakeGenerator
A snowflake generator written in Python. It's based on [Diffusion Limited Aggregation](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation).

Example creating 12 unique snowflakes:

```python
import numpy as np
from itertools import product
from SnowflakeGenerator import snowflake
for i,(angle, N) in enumerate(product([0,np.pi/12,np.pi/6],[40,50,60,70])):
    sf = snowflake(angle=angle)
    for _ in range(100):
        sf.add_crystal()
    sf.export(filename=f'{i}.svg',N=N, crystal_scale=1.7)
    sf.svg
```

Make a union of the exported circles, for instance using inkscape:

```bash
Inkscape --actions='EditSelectAllInAllLayers;SelectionUnion;SelectionSimplify;FileSave;FileClose' *.svg
```

