package no.tepohi.projectenturpublictransportapp

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.ArrayAdapter
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.PagerSnapHelper
import no.tepohi.projectenturpublictransportapp.databinding.ActivityMainBinding
import kotlin.math.min

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainActivityViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        var yours: Map<String, String>? = null


        viewModel.loadStops().observe(this) {
            Log.d("stops tag", it.toString())

            yours = it.associate { x -> x!!.name to x.id }

            Log.d("arraylist tag", yours.toString())

            val adapter = ArrayAdapter(
                this,
                android.R.layout.select_dialog_item,
                ArrayList(yours!!.keys),
//                4
            )

            binding.editTextFrom.setAdapter(adapter)
            binding.editTextTo.setAdapter(adapter)
        }


        binding.buttonResult.setOnClickListener {

            val from: String = binding.editTextFrom.text.toString()
            val to: String = binding.editTextTo.text.toString()

            if (from != "" && to != "") {



                viewModel.loadGraphQLData(yours!![from]!!, yours!![to]!!).observe(this) {

                    Log.d("tag", it.toString())

                    binding.textNumber.text = it.size.toString()
                    binding.recyclerviewVehicles.adapter = GraphQLAdapter(it)
                }
            }


        }

        binding.editTextTo.setOnEditorActionListener { _, actionID: Int, _ ->
            binding.editTextTo.dismissDropDown()
            hideKeyboard()
            actionID == EditorInfo.IME_ACTION_DONE
        }

        binding.editTextFrom.setOnEditorActionListener { _, actionID: Int, _ ->
            binding.editTextFrom.dismissDropDown()
            hideKeyboard()
            actionID == EditorInfo.IME_ACTION_DONE
        }

        binding.editTextTo.setOnClickListener {
            binding.editTextTo.dismissDropDown()
            hideKeyboard()


        }

        binding.editTextFrom.setOnClickListener {
            binding.editTextFrom.dismissDropDown()
            hideKeyboard()
        }

        PagerSnapHelper().attachToRecyclerView(binding.recyclerviewVehicles)
    }

    // Hides soft keyboard
    private fun hideKeyboard() {
        val view = this.currentFocus
        val imm = getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
        imm.hideSoftInputFromWindow(view?.windowToken,0)
    }

    fun idk() {

        val output = try {
            binding.editTextFrom.text.toString()
        } catch (e: Exception) {
            println("some error happened: $e")
            ""
        }

        viewModel.loadVehicles().observe(this) {

            Log.d("main tag", it.toString())
            var vehicles: List<Vehicle> = it

            if (output != "") {
                val condition = "RUT:Line:$output"
                Log.d("cond tag", condition)
                vehicles = vehicles.filter { vehicle -> vehicle.lineRef!!.line == condition}
            }

            vehicles = vehicles.sortedWith(compareBy { vehicle -> vehicle.id }).toMutableList()
            Log.d("main tag", vehicles.toString())

            binding.textNumber.text = vehicles.size.toString()
            binding.recyclerviewVehicles.adapter = VehicleAdapter(vehicles)
        }

    }
}

class LimitArrayAdapter<T>(
    context: Context,
    textViewResourceId: Int,
    objects: List<T>?,
    num: Int
): ArrayAdapter<T>(context, textViewResourceId, objects!!) {

    private val limit = num
    override fun getCount(): Int {
        return min(limit, super.getCount())
    }

}