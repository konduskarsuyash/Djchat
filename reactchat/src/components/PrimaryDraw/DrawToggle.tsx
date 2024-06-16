import React from 'react'
import { Box, IconButton } from '@mui/material'
import { ChevronLeft } from '@mui/icons-material'


const DrawToggle = () => {
  return (
    <Box sx={{
        height:'50px',
        display:'flex',
        justifyContent:'center',
        alignItems:'center',
        }}>
        <IconButton>
            <ChevronLeft/>
        </IconButton>
    </Box>
  )
}

export default DrawToggle