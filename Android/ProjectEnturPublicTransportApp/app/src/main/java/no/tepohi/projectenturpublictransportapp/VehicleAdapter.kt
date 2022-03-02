package no.tepohi.projectenturpublictransportapp

import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class VehicleAdapter(private val dataset: MutableList<Vehicle>): RecyclerView.Adapter<VehicleAdapter.ViewHolder>() {

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

    override fun onBindViewHolder(holder: ViewHolder, pos: Int) {

        holder.vehiclePosition.text = "${dataset[pos].position} ${dataset[pos].id}"
        holder.vehicleLineRef.text = dataset[pos].lineRef.toString()
        holder.vehicleProgress.text = dataset[pos].progress.toString()
    }

    override fun getItemCount() = dataset.size
}