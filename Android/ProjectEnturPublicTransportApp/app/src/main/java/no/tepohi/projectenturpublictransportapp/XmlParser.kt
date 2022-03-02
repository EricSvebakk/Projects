package no.tepohi.projectenturpublictransportapp

import android.util.Xml
import org.xmlpull.v1.XmlPullParser
import org.xmlpull.v1.XmlPullParserException
import java.io.IOException
import java.io.InputStream

class XmlParser {

    private val ns: String? = null

    @Throws(XmlPullParserException::class, IOException::class)
    fun parse(inputStream: InputStream): List<Vehicle> {
        inputStream.use {
            val parser: XmlPullParser = Xml.newPullParser()
            parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, false)
            parser.setInput(it, null)
            parser.nextTag()
            return readFeed(parser)
        }
    }

    @Throws(XmlPullParserException::class, IOException::class)
    private fun readFeed(parser: XmlPullParser): List<Vehicle> {
        val vehicleList = mutableListOf<Vehicle>()

        parser.require(XmlPullParser.START_TAG, ns, "Siri")

        var pbs: Progress? = null
        var mvj: LineRef? = null
        var vl: Position? = null
        var id: String? = null

        while (parser.next() != XmlPullParser.END_DOCUMENT) {

            if (parser.eventType != XmlPullParser.START_TAG) {
                if (parser.eventType == XmlPullParser.END_TAG && parser.name == "VehicleActivity") {
                    vehicleList.add(Vehicle(vl, mvj, pbs, id))

                    pbs = null
                    mvj = null
                    vl = null
                }
                continue
            }

//            Log.d("parser TAG", parser?.name)

            when (parser.name) {
                "ProgressBetweenStops" -> pbs = readProgressBetweenStops(parser)
                "MonitoredVehicleJourney" -> {
                    parser.require(XmlPullParser.START_TAG, ns, "MonitoredVehicleJourney")

                    var line: String? = null
                    var ref: String? = null

                    while (parser.next() != XmlPullParser.END_TAG) {
                        if (parser.eventType != XmlPullParser.START_TAG) {
                            continue
                        }
                        when (parser.name) {
                            "LineRef" -> line = readAttribute(parser, parser.name)
                            "DirectionRef" -> ref = readAttribute(parser, parser.name)
                            "VehicleLocation" -> vl = readVehicleLocation(parser)
                            "VehicleRef" -> id = readAttribute(parser, parser.name)
                            else -> skip(parser)
                        }
                    }

                    mvj = LineRef(line, ref)
                }
                else -> continue
            }
        }

        return vehicleList
    }


    @Throws(IOException::class, XmlPullParserException::class)
    private fun readProgressBetweenStops(parser: XmlPullParser): Progress {

        parser.require(XmlPullParser.START_TAG, ns, "ProgressBetweenStops")

        var distance: String? = null
        var progress: String? = null

        while (parser.next() != XmlPullParser.END_TAG) {
            if (parser.eventType != XmlPullParser.START_TAG) {
                continue
            }

            when (parser.name) {
                "LinkDistance" -> distance = readAttribute(parser, parser.name)
                "Percentage" -> progress = readAttribute(parser, parser.name)
                else -> skip(parser)
            }
        }

        return Progress(distance, progress)
    }


    @Throws(IOException::class, XmlPullParserException::class)
    private fun readVehicleLocation(parser: XmlPullParser): Position {

        var latitude: String? = null
        var longitude: String? = null

        while (parser.next() != XmlPullParser.END_TAG) {
            if (parser.eventType != XmlPullParser.START_TAG) {
                continue
            }
            when (parser.name) {
                "Latitude" -> latitude = readAttribute(parser, parser.name)
                "Longitude" -> longitude = readAttribute(parser, parser.name)
                else -> skip(parser)
            }
        }

        return Position(latitude, longitude)
    }

    @Throws(IOException::class, XmlPullParserException::class)
    private fun readAttribute(parser: XmlPullParser, tag: String): String {
        parser.require(XmlPullParser.START_TAG, ns, tag)
        val attribute = readText(parser)
        parser.require(XmlPullParser.END_TAG, ns, tag)
        return attribute
    }

    @Throws(IOException::class, XmlPullParserException::class)
    private fun readText(parser: XmlPullParser): String {
        var result = ""
        if (parser.next() == XmlPullParser.TEXT) {
            result = parser.text
            parser.nextTag()
        }
        return result
    }

    @Throws(XmlPullParserException::class, IOException::class)
    private fun skip(parser: XmlPullParser) {
        if (parser.eventType != XmlPullParser.START_TAG) {
            throw IllegalStateException()
        }
        var depth = 1
        while (depth != 0) {
            when (parser.next()) {
                XmlPullParser.END_TAG -> depth--
                XmlPullParser.START_TAG -> depth++
            }
        }
    }
}

data class Vehicle(val position: Position?, val lineRef: LineRef?, val progress: Progress?, val id: String?)
data class Position(val Latitude: String?, val Longitude: String?)
data class LineRef(val line: String?, val direction: String?)
data class Progress(val LinkDistance: String?, val Percentage: String?)
