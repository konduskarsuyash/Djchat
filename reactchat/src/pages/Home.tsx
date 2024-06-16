import React from 'react'
import { Box,CssBaseline } from '@mui/material'
import PrimaryAppBar from './template/PrimaryAppBar'


const Home = () => {

  return (
  <Box sx={{display:"flex"}}>
    <CssBaseline/>
    <PrimaryAppBar/>
    Home
  </Box>
  )
}

export default Home