## Fast Start  (Requires Python3 and Curl)


### Up and Running in Less Than Thirty-Seven Seconds


* pip install threefive
```go
pip install threefive


```
* Parse SCTE 35 and PTS data from a video over the network
```js
 curl -s https://futzu.com/mpegwithscte35.ts -o - | python3 -c 'import threefive; threefive.decode()' 
```


