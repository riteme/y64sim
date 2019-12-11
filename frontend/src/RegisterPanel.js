import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Typography
} from '@material-ui/core'

import StatusText from './StatusText'

const useStyles = makeStyles(theme => ({
  root: {
    tableLayout: 'fixed'
  },
  header: {
    backgroundColor: theme.palette.grey[300]
  },
  names: {
    width: '25%'
  },
  na: {
    color: theme.palette.text.hint,
    padding: [[theme.spacing(1), theme.spacing(3), theme.spacing(3)]]
  }
}))

function RegisterPanel({
  data,
  translateState
}) {
  const classes = useStyles();

  if (data === null || data === undefined) return (
    <Typography variant="body1" className={classes.na}>Not Available</Typography>
  );

  let rows = []
  for (const key in data) {
    const [value, hex] = data[key];

    rows.push(
      <TableRow key={key}>
        <TableCell
          component="th"
          scope="row"
          align="center"
        >{key}</TableCell>
        {
          translateState && key === 'state' ?
          <React.Fragment>
            <TableCell align="right">
              <StatusText state={parseInt(value)} />
            </TableCell>
            <TableCell align="right">(Not Available)</TableCell>
          </React.Fragment>
        :
          <React.Fragment>
            <TableCell align="right">{value}</TableCell>
            <TableCell align="right">{hex === null ? '(Not Available)' : `0x${hex}`}</TableCell>
          </React.Fragment>
        }
      </TableRow>
    )
  }

  return (
    <Table
      size="small"
      classes={{root: classes.root}}
    >
      <TableHead className={classes.header}>
        <TableRow>
          <TableCell align="center" className={classes.names}>Name</TableCell>
          <TableCell align="right">Value</TableCell>
          <TableCell align="right">Hexadecimal</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows}
      </TableBody>
    </Table>
  )
}

export default RegisterPanel;