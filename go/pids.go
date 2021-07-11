package threefive

//Pids holds collections of pids by type for threefive.Stream.
type Pids struct {
	PmtPids    []uint16
	PcrPids    []uint16
	Scte35Pids []uint16
}

func (pids *Pids) isPmtPid(pid uint16) bool {
	return isIn16(pids.PmtPids, pid)
}

func (pids *Pids) addPmtPid(pid uint16) {
	if !pids.isPmtPid(pid) {
		pids.PmtPids = append(pids.PmtPids, pid)
	}
}

func (pids *Pids) isPcrPid(pid uint16) bool {
	return isIn16(pids.PcrPids, pid)
}

func (pids *Pids) addPcrPid(pid uint16) {
	if !pids.isPcrPid(pid) {
		pids.PcrPids = append(pids.PcrPids, pid)
	}
}

func (pids *Pids) isScte35Pid(pid uint16) bool {
	return isIn16(pids.Scte35Pids, pid)
}

func (pids *Pids) addScte35Pid(pid uint16) {
	if !(pids.isScte35Pid(pid)) {
		pids.Scte35Pids = append(pids.Scte35Pids, pid)
	}
}
func (pids *Pids) delScte35Pid(pid uint16) {
	n := 0
	for _, val := range pids.Scte35Pids {
		if val != pid {
			pids.Scte35Pids[n] = val
			n++
		}
	}

	pids.Scte35Pids = pids.Scte35Pids[:n]
}
