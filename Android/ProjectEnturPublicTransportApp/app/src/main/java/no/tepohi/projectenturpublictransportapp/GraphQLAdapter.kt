package no.tepohi.projectenturpublictransportapp

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import no.tepohi.example.FindTripQuery

class GraphQLAdapter(private val dataset: MutableList<FindTripQuery.TripPattern>): RecyclerView.Adapter<GraphQLAdapter.ViewHolder>() {

    class ViewHolder(view: View): RecyclerView.ViewHolder(view) {
        val vehiclePosition: TextView
        val vehicleLineRef: TextView
        val vehicleProgress: TextView

        init {
            vehiclePosition = view.findViewById(R.id.text_position)
            vehicleLineRef = view.findViewById(R.id.text_lineRef)
            vehicleProgress = view.findViewById(R.id.text_progress)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.vehicle_element, parent, false)

        return ViewHolder(view)
    }

    @SuppressLint("SetTextI18n")
    override fun onBindViewHolder(holder: ViewHolder, pos: Int) {

        val text = (dataset[pos].duration.toString().toInt() / 60.0).toFloat()

        holder.vehiclePosition.text = "Estimated walking: ${dataset[pos].walkDistance!!.toInt()}m"
        holder.vehicleLineRef.text = "Duration: ${text.toInt()}min"

        var string = ""
        dataset[pos].legs.forEach {

            val line = if (it?.line != null) it.line.id.split(":")[2] else ""
            val name = if (it?.line?.name != null) "(${it.line.name})" else ""

            string +=  "${it?.mode} $line $name\n"
        }

        holder.vehicleProgress.text = string.trim()
    }

    override fun getItemCount() = dataset.size
}