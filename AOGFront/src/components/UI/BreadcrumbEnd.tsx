interface Props {
    name: string
}

function BreadcrumbEnd({name}: Props) {
  return (
    <li className="text-gray-800 text-base font-bold cursor-pointer">
        {name}
    </li>
  )
}

export default BreadcrumbEnd