package threefive

import (
	"bytes"
	"fmt"
	"os"
)

type Pids struct {
	pmt    []uint16
	pcr    []uint16
	scte35 []uint16
	ignore []uint16
}

func (pids *Pids) isPmt(pid uint16) bool {
	return IsIn16(pids.pmt, pid)
}
func (pids *Pids) isPcr(pid uint16) bool {
	return IsIn16(pids.pcr, pid)
}
func (pids *Pids) isScte35(pid uint16) bool {
	return IsIn16(pids.scte35, pid)
}

func (pids *Pids) isIgnore(pid uint16) bool {
	return IsIn16(pids.ignore, pid)
}

type Stream struct {
	Pkts     int
	pid2prgm map[uint16]uint16
	prgm2pcr map[uint16]uint64
	prgm2pts map[uint16]uint64
	partial  map[uint16][]byte
	last     map[uint16][]byte
	pids     Pids
}

func (stream *Stream) mkMaps() {
	stream.pid2prgm = make(map[uint16]uint16)
	stream.last = make(map[uint16][]byte)
	stream.partial = make(map[uint16][]byte)
	stream.prgm2pcr = make(map[uint16]uint64)
	stream.prgm2pts = make(map[uint16]uint64)
}

// Decode for Stream
func (stream *Stream) Decode(fname string) {
	stream.mkMaps()
	stream.Pkts = 0
	file, err := os.Open(fname)
	Chk(err)
	defer file.Close()
	buffer := make([]byte, BufferSize)
	for {
		bytesread, err := file.Read(buffer)
		if err != nil {
			break
		}
		for i := 1; i <= (bytesread / PktSz); i++ {
			end := i * PktSz
			start := end - PktSz
			pkt := buffer[start:end]
			stream.Pkts += 1
			stream.parse(pkt)
		}
	}
	// fmt.Printf("%+v",stream)
}

func (stream *Stream) mkPcr(prgm uint16) float64 {
	pcrb := stream.prgm2pcr[prgm]
	return mk90k(pcrb)
}

func (stream *Stream) mkPts(prgm uint16) float64 {
	pts := stream.prgm2pts[prgm]
	return mk90k(pts)
}

func (stream *Stream) parsePusi(pkt []byte) bool {
	if (pkt[1]>>6)&1 == 1 {
		if pkt[6]&1 == 1 {
			return true
		}
	}
	return false
}

func (stream *Stream) parsePts(pkt []byte, pid uint16) {
	if stream.parsePusi(pkt) {
		var ok bool
		var prgm uint16
		prgm, ok = stream.pid2prgm[pid]
		if ok {
			pts := (uint64(pkt[13]) >> 1 & 7) << 30
			pts |= uint64(pkt[14]) << 22
			pts |= (uint64(pkt[15]) >> 1) << 15
			pts |= uint64(pkt[16]) << 7
			pts |= uint64(pkt[17]) >> 1
			stream.prgm2pts[prgm] = pts
			return
		}
	}
	return
}

func (stream *Stream) parsePcr(pkt []byte, pid uint16) {
	if (pkt[3]>>5)&1 == 1 {
		if (pkt[5]>>4)&1 == 1 {
			pcr := (uint64(pkt[6]) << 25)
			pcr |= (uint64(pkt[7]) << 17)
			pcr |= (uint64(pkt[8]) << 9)
			pcr |= (uint64(pkt[9]) << 1)
			pcr |= uint64(pkt[10]) >> 7
			prgm := stream.pid2prgm[pid]
			stream.prgm2pcr[prgm] = pcr
			return
		}
	}
	return
}

func (stream *Stream) parsePayload(pkt []byte) []byte {
	head := 4
	afc := (pkt[3] >> 5) & 1
	if afc == 1 {
		afl := int(pkt[4])
		head += afl + 1
	}
	if head > PktSz {
		head = PktSz
	}
	return pkt[head:]
}

func (stream *Stream) plusPartial(pay []byte, pid uint16, bite byte) []byte {
	var ok bool
	var val []byte
	val, ok = stream.partial[pid]
	if ok {
		return append(val, pay...)
	}
	return splitByIdx(pay, bite)
}

func (stream *Stream) sameAsLast(pay []byte, pid uint16) bool {
	var ok bool
	var val []byte
	val, ok = stream.last[pid]
	if ok {
		if bytes.Compare(pay, val) == 0 {

			return true
		}
	}
	stream.last[pid] = pay
	return false
}

func (stream *Stream) sectionDone(pay []byte, pid uint16, seclen uint16) bool {
	if seclen+3 > uint16(len(pay)) {
		stream.partial[pid] = pay

		return false
	}

	return true
}

// Parser for Stream
func (stream *Stream) parse(pkt []byte) {
	p := parsePid(pkt[1], pkt[2])
	pid := &p
	pay := stream.parsePayload(pkt)
	if *pid == 0 {
		stream.parsePat(pay, *pid)
	}
	if stream.pids.isPmt(*pid) {
		stream.parsePmt(pay, *pid)
	}
	if stream.pids.isPcr(*pid) {
		stream.parsePcr(pkt, *pid)
	} else {
		stream.parsePts(pkt, *pid)
	}
	if stream.pids.isScte35(*pid) {
		stream.parseScte35(pay, *pid)
	}
}

func (stream *Stream) parsePat(pay []byte, pid uint16) {
	if stream.sameAsLast(pay, pid) {
		return
	}
	pay = stream.plusPartial(pay, pid, 0x00)
	// pointer field = pay[0]
	// table_id  = pay[1]
	seclen := parseLen(pay[2], pay[3])
	if !stream.sectionDone(pay, pid, seclen) {
		return
	}
	seclen -= 5 // pay bytes 4,5,6,7,8
	idx := uint16(9)
    end := idx +seclen -4  //  4 bytes for crc
	chunksize := uint16(4)
	for idx < end {
		prgm := parsePrgm(pay[idx], pay[idx+1])
		if prgm > 0 {
			pmtpid := parsePid(pay[idx+2], pay[idx+3])
			if !stream.pids.isPmt(pmtpid) {
				stream.pids.pmt = append(stream.pids.pmt, pmtpid)
				fmt.Printf("Program: %v Pmt Pid: %v\n", prgm, pmtpid)
			}
		}
        idx += chunksize

	}
	delete(stream.partial, pid)
}

func (stream *Stream) parsePmt(pay []byte, pid uint16) {
	if stream.sameAsLast(pay, pid) {
		return
	}
	pay = stream.plusPartial(pay, pid, 0x02)
	if len(pay) == 0 {
		return
	}
	secinfolen := parseLen(pay[1], pay[2])
	if !stream.sectionDone(pay, pid, secinfolen) {
		return
	}
	prgm := parsePrgm(pay[3], pay[4])
	pcrpid := parsePid(pay[8], pay[9])
	if !(stream.pids.isPcr(pcrpid)) {
		stream.pids.pcr = append(stream.pids.pcr, pcrpid)
	}
	proginfolen := parseLen(pay[10], pay[11])
	idx := uint16(12)
	idx += proginfolen
	silen := secinfolen - 9
	silen -= proginfolen
	stream.parseStreams(silen, pay, idx, prgm)
	delete(stream.partial, pid)
	return
}

func (stream *Stream) parseScte35(pay []byte, pid uint16) {
	pay = stream.plusPartial(pay, pid, 0xfc)
	if len(pay) == 0 {
		return
	}
	seclen := parseLen(pay[1], pay[2])
	if !stream.sectionDone(pay, pid, seclen) {
			return
	}
	cue := stream.mkCue(pid)
	if !cue.Decode(pay){
	    return
	 }
    cue.Show()
	delete(stream.partial, pid)
}

func (stream *Stream) mkCue(pid uint16) Cue {
	var cue Cue
	cue.Pid = pid
	prgm := stream.pid2prgm[pid]
	cue.Program = prgm
	cue.Pcr = stream.mkPcr(prgm)
	cue.Pts = stream.mkPts(prgm)
	cue.PacketNumber = stream.Pkts
	return cue
}

func (stream *Stream) parseStreams(silen uint16, pay []byte, idx uint16, prgm uint16) {
	chunksize := uint16(5)
	endidx := (idx + silen) - chunksize
	for idx < endidx {
		streamtype := pay[idx]
		elpid := parsePid(pay[idx+1], pay[idx+2])
		eilen := parseLen(pay[idx+3], pay[idx+4])
		idx += chunksize
		idx += eilen
		//fmt.Printf(" Pid: %#x Stream Type: %v\n",elpid, streamtype)
		stream.pid2prgm[elpid] = prgm
		stream.vrfyStreamType(elpid, streamtype)
	}

}

func (stream *Stream) vrfyStreamType(pid uint16, streamtype uint8) {
    if streamtype == 134 {
		if !(stream.pids.isScte35(pid)) {
			stream.pids.scte35 = append(stream.pids.scte35, pid)
		}

	}
}
