import React from 'react'
import { withStyles } from '@material-ui/core/styles'

import {
  CircularProgress
} from '@material-ui/core'

const styles = {
  content: {
    display: 'flex',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'center'
  }
}

class Presentation extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.content}>
        <CircularProgress />
      </div>
    )
  }
}

export default withStyles(styles)(Presentation);