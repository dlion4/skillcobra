import React from 'react'
import { getCategories } from '../actions'

const Sitemap = ({id}: {id: string}) => {
  const query = getCategories()
  console.log(query)
  return (
    <div>Sitemap</div>
  )
}

export  {Sitemap}