
### 35 decode, command line SCTE35 decoder.

>type 'make cli' or 'make pypy3-cli' as root to install to /usr/local/bin

#### use like:
```fortran
cat myvideo.ts | 35decode
```
```fortran
35decode https://futzu.com/xaa.ts
```
```fortran
35decode ~/myvideo.ts https://futzu.com/xaa.ts someothervideo.ts 
```
```fortran
35decode mpegts_dir/*.ts
```
 ```fortran
35decode '/DBZAAAAAAAA///wBQb+AAAAAABDAkFDVUVJAAAACn//AAApMuAPLXVybjp1dWlkOmFhODViYmI2LTVjNDMtNGI2YS1iZWJiLWVlM2IxM2ViNzk5ORAAAFz7UQA='
    ```
