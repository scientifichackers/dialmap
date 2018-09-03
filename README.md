# Dial Map

Ever had to deal with the horrible jitter associated with using Potentiometers with an ADC? 

Then this library is just for you.

*Dial Map lets you program "Dead Zones" into your Dials, eliminating the need for crazy software/hardware filters for removing jitter.*

- Automatically normalizes the ADC's raw values.
- 100% Dependency free, MicroPython compatible.
- Fast, because of the magic that is static mappings.

## Install

It's a sub-100 line python script so, just copy-paste [dialmap.py](dialmap.py) and import it. 

## Background

Potentiometers *always* seem have some degree of jitter.
 
It doesn't matter much in the Analog world,
but when you want to use them for Digital (especially Software applications), 
this is a *huge* headache.

### The Problem

We have an ADC that gives us the reading of potentiometer as an integer between `0` and `1000`, 
and we want to map these values to a range between `1` and `5`. 

Here is a visual representation:

```text
                    +------+-------+-------+-------+-------+
Interpreted Value:  |  1   |   2   |   3   |   4   |   5   |     
                    +------+-------+-------+-------+-------+
Raw Value:          0     200     400     600     800     1000
                         ↑↑↑↑↑
```


*It's guaranteed that the potentiometer will have some amount of jitter, even when it's absolutely stationary.*

---

Let's assume that the values are swinging around the `200` mark. (represented very creatively by the arrows)

Even the slightest amount of jitter will cause random switching between `1` and `2`, 
causing unwanted behavior in our software.

**I mean Just imagine your IOT Fan controlled by this knob!**

### The culprit

However big or small the jitter, the fact that we have the concept of "breakpoints" is damaging.

### The Solution


The solution, is to program "Dead Zones" into our mapping.

When-ever the raw value reaches the "Dead Zone", our Software should stop responding to changes.

Here is a visual representation:

```text
                    +-------+---+-------+---+-------+---+-------+---+-------+
Interpreted Value:  |   1   |XXX|   2   |XXX|   3   |XXX|   4   |XXX|   5   |     
                    +-------+---+-------+---+-------+---+-------+---+-------+
Raw Value:          0      195 205     396 405     595 605     795 805     1000
                          ↑↑↑↑↑                          
```

Now even if there is jitter at the `200` mark, 
the interpreted value will remain stable at `1` as long as there is a jitter of `±5`.


## Example
 
```python
from dialmap import DialMap

my_dial_map = DialMap(output_pts=range(5), deadzone=20)
```

- `deadzone` is in percentage. 
    Such that, `0` results in no deadzones, and a value of `100` results in no active zones (empty mapping).

- The `DialMap` has adaptive normalization. 
    Which means it will observe the range of ADC's raw values, and normalize them automatically. 
    Which means, you don't need to provide the range of ADC's raw values.
  
Here is how you use this mapping:

```python
my_dial_map.translate(150)
```

And that's it!


You can inspect the mapping like this:

```python
>> my_dial_map.mapping.keys()
dict_keys([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99])

>>> my_dial_map.mapping.values()
dict_values([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
```

- `keys()` represent the normalized values.
- `values()` represent the `output_pts` you asked for.

The `DialMap.translate()` simply normalizes the input, and passes it through this mapping.

If a Dead Zone is encountered, (for e.g. `16` is a Dead Point above) then the last translated value is returned.

---

<a href="https://www.buymeacoffee.com/u75YezVri" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

[🐍🏕️](http://www.pycampers.com/)
