import { ItemProp } from "../../types/global"
import DataTable from "react-data-table-component"

function TableDataUI({item}: ItemProp) {
  const colums = [
    {
      name: 'Name',
      selector: row => row.name,
    },
    {
      name: 'Model',
      selector: row => row.model,
    },
    {
      name: 'Serials',
      selector: row => row.serials,
    },
    {
      name: 'Cost',
      selector: row => row.cost,
    },
    {
      name: 'Date purchased',
      selector: row => row.date_purchased,
    },
    {
      name: 'Created',
      selector: row => row.created,
    },
    {
      name: 'Actions',
      selector: row => row.actions,
    },
  ]

  const data = [
    {
      id: `${item.id}`,
      name: `${item.name}`,
      model: `${item.model}`,
      serial: `${item.serials}`,
      cost: `${item.cost}`,
      data_purchased: `${item.date_purchased}`,
      created: `${item.created}`,
      actions: <button>Edit</button>
    }
  ]
  return (
    <DataTable columns={colums} data={data} />
  )
}

export default TableDataUI