package threefive

//Pids holds collections of pids by type for threefive.Stream.
type Pids struct {
	pmt    []uint16
	pcr    []uint16
	scte35 []uint16
}

func (pids *Pids) isPmt(pid uint16) bool {
	return IsIn16(pids.pmt, pid)
}

func (pids *Pids) addPmt(pid uint16) {
	if !pids.isPmt(pid) {
		pids.pmt = append(pids.pmt, pid)
	}
}

func (pids *Pids) isPcr(pid uint16) bool {
	return IsIn16(pids.pcr, pid)
}

func (pids *Pids) addPcr(pid uint16) {
	if !pids.isPcr(pid) {
		pids.pcr = append(pids.pcr, pid)
	}
}

func (pids *Pids) isScte35(pid uint16) bool {
	return IsIn16(pids.scte35, pid)
}

func (pids *Pids) addScte35(pid uint16) {
	if !(pids.isScte35(pid)) {
		pids.scte35 = append(pids.scte35, pid)
	}
}
