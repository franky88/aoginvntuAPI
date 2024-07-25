import { ReactNode } from "react"

interface Props {
    children: ReactNode;
}

function Breadcrumbs({children}: Props) {
  return (
    <ul className="flex items-center font-[sans-serif] space-x-4 mt-4">
        {children}
    </ul>
  )
}

export default Breadcrumbs