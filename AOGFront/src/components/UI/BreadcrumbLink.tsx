import { Link } from "react-router-dom"

interface Props {
    link: string,
    name: string
}

function BreadcrumbLink({link, name}: Props) {
  return (
    <li className="text-blue-500 text-base cursor-pointer">
        <Link to={link}>{name}</Link> 
    </li>
  )
}

export default BreadcrumbLink