import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  Typography,
  Slider,
  Switch
} from '@material-ui/core'

const useStyles = makeStyles(theme => ({
  settings: {
    padding: [[theme.spacing(2), theme.spacing(5)]]
  },
  options: {
    display: 'flex'
  },
  optionText: {
    display: 'flex',
    alignItems: 'center',
    flexGrow: 1
  }
}))

function Settings({
  simulationInterval,
  useLegacyMemoryPanel,
  onSetSimulationInterval,
  onSetUseLegacyMemoryPanel
}) {
  const classes = useStyles();

  return (
    <div>
      <div className={classes.settings}>
        <Typography variant="subtitle1">
          Simulation step interval:
        </Typography>
        <Slider
          getAriaValueText={value => `${value}ms`}
          value={simulationInterval}
          valueLabelDisplay="auto"
          step={50}
          min={50}
          max={5000}
          marks={[
            {value: 50, label: '50ms'},
            {value: 1000, label: '1s'},
            {value: 2000, label: '2s'},
            {value: 3000, label: '3s'},
            {value: 4000, label: '4s'},
            {value: 5000, label: '5s'}
          ]}
          onChange={onSetSimulationInterval}
        />
      </div>
      <div className={[
        classes.settings,
        classes.options
      ].join(' ')}>
        <Typography variant="subtitle1" className={classes.optionText}>
          Use legacy memory panel:
        </Typography>
        <Switch
          checked={useLegacyMemoryPanel}
          onChange={onSetUseLegacyMemoryPanel}
          color="primary"
        />
      </div>
    </div>
  )
}

export default Settings;