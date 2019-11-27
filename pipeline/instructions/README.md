PRINCIPLE: assume executed in normal state and raise exceptions when any error occurs. **Exceptions are requests** to pipeline system. Pipeline logic will resolve any hazards reported by exceptions.

Pipeline register `stat` is maintained by pipeline logic. **DO NOT TOUCH THEM**.

`NOP` is the base class of all other instructions since `NOP` actually does nothing.

KEEP IN MIND:

1. Lock resources in Decode Stage.
2. Handle forwarding in Execute Stage & Memory Stage & Write Stage.
3. Unlock resources in Execute Stage (for CC) & Memory Stage & Write Stage.
4. PC prediction & correction logic.