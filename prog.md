   <details><summary>Mpegts Multicast in three lines of code.</summary>

```python3
import threefive

strm = threefive.Stream('udp://@239.35.0.35:1234')
strm.decode()
````
  _(need an easy multicast server?_ [gumd](https://github.com/futzu/gumd) )

---

  </details>


 <details><summary>Mpegts over Https in three lines of code.</summary>


```python3
import threefive
strm = threefive.Stream('https://iodisco.com/ch1/ready.ts')
strm.decode()
```

       
   </details>


 <details><summary>Base64 in five lines of code.</summary>


```python3
>>> from threefive import Cue
>>> stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
>>> cue=Cue(stuff)
>>> cue.decode()
True
 >>> cue.show()

```
---
   </details>

 <details><summary>Bytes in five lines of code.</summary>

```python3
>>> import threefive

>>> stuff = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
>>> cue=Cue(stuff)
>>> cue.decode()
True
>>> cue.show()
```
---


   </details>



<details><summary>Hex in 4 lines of code.</summary>


```python3
import threefive

cue = threefive.Cue("0XFC301100000000000000FFFFFF0000004F253396")
cue.decode()
cue.show()
```

---

</details>
