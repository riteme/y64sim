const MASK = 0xFFFFFFFF;
const BASE = 23333;
const COEFF = 17892

export function buildMemoryTree(mem) {
  function _build(left, right) {
    if (left === right) return {
      left: left,
      right: right,
      value: parseInt(mem[left], 16),
      literal: mem[left]
    };
    const mid = (left + right) >> 1;
    const lch = _build(left, mid);
    const rch = _build(mid + 1, right);
    return {
      left: left,
      right: right,
      value: ((lch.value * BASE & MASK) + rch.value) * COEFF & MASK,
      lch: lch,
      rch: rch
    };
  }
  return _build(0, mem.length - 1);
}