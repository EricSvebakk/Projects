package no.tepohi.projectenturpublictransportapp

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import no.tepohi.example.FindTripQuery
import no.tepohi.example.StopsQuery

class MainActivityViewModel: ViewModel() {

    private val dataSource = DataSource()

    private val vehicleData = MutableLiveData<MutableList<Vehicle>>()
    private val graphQLData = MutableLiveData<MutableList<FindTripQuery.TripPattern>>()
    private val stopsData = MutableLiveData<MutableList<StopsQuery.StopPlace?>>()

    fun loadVehicles(): LiveData<MutableList<Vehicle>> {

        viewModelScope.launch(Dispatchers.IO) {
            Log.d("load Vehicles tag+", "done!")
            dataSource.fetchVehicles().also {
                vehicleData.postValue(it)
            }
        }
        Log.d("load Vehicles tag", "done!")

        return vehicleData
    }

    fun loadGraphQLData(from: String, to: String): LiveData<MutableList<FindTripQuery.TripPattern>> {

        viewModelScope.launch(Dispatchers.IO) {
            Log.d("load Vehicles tag+", "done!")
            dataSource.fetchGraphQLData(from, to).also {
                graphQLData.postValue(it)
            }
        }
        Log.d("load Vehicles tag", "done!")

        return graphQLData
    }

    fun loadStops(): MutableLiveData<MutableList<StopsQuery.StopPlace?>> {

        viewModelScope.launch(Dispatchers.IO) {
            dataSource.fetchStops().also {
                stopsData.postValue(it)
            }
        }

        return stopsData
    }
}