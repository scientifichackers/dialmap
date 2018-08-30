# Dial Map
*Software controlled dials done right.*

Ever had to deal with potentiometers, and their horrible jitter? 
Then this library is just for you.

### The Problem

Potentiometers always have some degree of jitter.
 
It doesn't matter much in the Analog world,
but when you want to use them for Digital (especially Software applications), 
this is a *huge* headache.

**Let's take an example**

We have an ADC that gives us the reading of potentiometer as an integer between `0` and `1024`, 
and we want to map these values to a range between `1` and `5`. 

Here is a visual representation:

```text
                    +------+-------+-------+-------+-------+
Interpreted Value:  |  1   |   2   |   3   |   4   |   5   |     
                    +------+-------+-------+-------+-------+
Raw Value:          0     200     400     600     800     1024
                         ↑↑↑↑↑
```


*It's guaranteed that the potentiometer will have some amount of jitter, even when it's absolutely stationary.*

Let's assume that the values are swinging around the `200` mark. (represented very creatively by the arrows)

You can immediately notice the problem here. 

Even the slightest amount of jitter will cause random switching between `1` and `2`, 
causing unwanted behavior in our software.

**I mean Just imagine your IOT Fan controlled by this knob!**

### The culprit

However big or small the jitter, the fact that we have the concept of "breakpoints" is damaging.

### The Solution


The solution, is to program "Dead Zones" into our mapping.

When-ever the raw value reaches the "Dead Zone", our Software will stop responding.

Here is a visual representation:

```text
                    +-------+---+-------+---+-------+---+-------+---+-------+
Interpreted Value:  |   1   |XXX|   2   |XXX|   3   |XXX|   4   |XXX|   5   |     
                    +-------+---+-------+---+-------+---+-------+---+-------+
Raw Value:          0      200 210     400 410     600 610     800 810     1024
                          ↑↑↑↑↑                          
```

Now even if there is jitter at the `200` mark, 
the interpreted value will remain stable at `1` as long as there is a jitter of `±10`.

Here's how you can do that in code 
```python
import dialmap

my_dial_map = dialmap.DialMap(output_range=(1, 5), deadzone=5)
```

- `deadzone` is in percentage. (`10 / 200 * 100 == 5`)
- The `DialMap` class has adaptive normalization. 
  Which means it will observe the range of ADC raw values, and normalize them automatically in between 0 to 100. 