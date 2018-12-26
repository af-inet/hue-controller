# hue controller

wip hue controller

**setup**

```bash
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

**register with your hue bridge**

(you'll be prompted to press the button on the hue bridge)

```bash
python hue_configure.py
```

**run a light show**

```bash
python hue_sequence.py
```
