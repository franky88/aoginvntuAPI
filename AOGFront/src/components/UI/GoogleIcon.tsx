interface Props {
    iconName: string,
    clsName: string
}

function GoogleIcon({iconName, clsName}: Props) {
  return (
    <span className={`material-symbols-outlined ${clsName}`}>{iconName}</span>
  )
}

export default GoogleIcon