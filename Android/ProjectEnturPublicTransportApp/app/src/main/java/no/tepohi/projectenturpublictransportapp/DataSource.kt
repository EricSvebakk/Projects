package no.tepohi.projectenturpublictransportapp

import android.util.Log
import com.apollographql.apollo3.ApolloClient
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.coroutines.awaitString
import no.tepohi.example.FindTripQuery
import no.tepohi.example.StopsQuery
import java.lang.Exception

class DataSource {

    private val path = "https://api.entur.io/journey-planner/v3/graphql"
    private val apolloClient = ApolloClient.Builder().serverUrl(path).build()

    suspend fun fetchVehicles(): MutableList<Vehicle> {

        val path = "https://api.entur.io/realtime/v1/rest/vm?datasetId=RUT"

        val result = try {
            val response = Fuel.get(path).awaitString()
            Log.d("xml string tag", response)

            val responseParsed = XmlParser().parse(response.byteInputStream())
            Log.d("xml parsed tag", responseParsed.toString())
            responseParsed
        }

        catch (e: Exception) {
            println("A network request exception was thrown: ${e.message}")
            listOf(Vehicle(Position("0.0", "0.0"), LineRef("", ""), Progress("", ""), ""))
        }

        Log.d("vehicle object tag", result.toString())

        return result.toMutableList()
    }

    suspend fun fetchGraphQLData(from: String, to: String): MutableList<FindTripQuery.TripPattern> {

        val response = try {
            val query = FindTripQuery(from, to)
            val temp = apolloClient.query(query).execute()
            temp.data?.trip?.tripPatterns?.toMutableList() ?: emptyList<FindTripQuery.TripPattern>().toMutableList()
        }

        catch (e: Exception) {
            println("A network request exception was thrown: ${e.message}")
            emptyList<FindTripQuery.TripPattern>().toMutableList()
        }

        return response
    }

    suspend fun fetchStops(): MutableList<StopsQuery.StopPlace?> {

        val response = try {
            val temp = apolloClient.query(StopsQuery()).execute()
            temp.data?.stopPlaces?.toMutableList() ?: emptyList<StopsQuery.StopPlace?>().toMutableList()
        }

        catch (e: Exception) {
            println("A network request exception was thrown: ${e.message}")
            emptyList<StopsQuery.StopPlace?>().toMutableList()
        }

        Log.d("fetchStops tag", response.toString())
        return response
    }
}