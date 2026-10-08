type KpiCardProps = {
  label: string
  value: number | string
}

function KpiCard({ label, value }: KpiCardProps) {
  return (
    <div className="kpi-card">
      <p>{label}</p>
      <h2>{value}</h2>
    </div>
  )
}

export default KpiCard
