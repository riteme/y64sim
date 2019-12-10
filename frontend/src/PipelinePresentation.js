import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  CircularProgress
} from '@material-ui/core'

const useStyles = makeStyles({
  content: {
    display: 'flex',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'center'
  }
})

function PipelinePresentation(props) {
  const classes = useStyles();

  return (
    <div className={classes.content}>
      <CircularProgress />
    </div>
  )
}

export default PipelinePresentation;