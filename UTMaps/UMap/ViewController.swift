//
//  ViewController.swift
//  UMap
//
//  Created by Yecheng Song on 2017-09-16.
//  Copyright © 2017 Yecheng Song. All rights reserved.
//

import UIKit
import GoogleMaps

class Building: NSObject {
    let name: String
    let location: CLLocationCoordinate2D
    let zoom: Float
    let snippet: String
    let count: Int
    
    init(name: String, location: CLLocationCoordinate2D, zoom: Float, snippet: String) {
        self.name = name
        self.location = location
        self.zoom = zoom
        self.count = 0
        self.snippet = snippet
    }
}


var uoftDict = ["AB": Building(name: "Astronomy and Astrophysics",
                               location: CLLocationCoordinate2DMake(43.660474, -79.39745),
                               zoom: 15.75,
                               snippet: "--"),
                
                "AD": Building(name: "Enrolment Services",
                               location: CLLocationCoordinate2DMake(43.668097, -79.400255),
                               zoom: 15.75,
                               snippet: "--"),
                
                
                "SS": Building(name: "Sidney Smith Hall",
                             location: CLLocationCoordinate2DMake(43.662668, -79.398465),
                             zoom: 15.75,
                             snippet: "--"),

                "SU": Building(name: "40 Sussex Ave.",
                             location: CLLocationCoordinate2DMake(43.66495, -79.401796),
                             zoom: 15.75,
                             snippet: "--"),

                
                
                
                
                
                "TC": Building(name: "Trinity College",
                             location: CLLocationCoordinate2DMake(43.665062, -79.395548),
                             zoom: 15.75,
                             snippet: "--"),
                
                "TF": Building(name: "Teefy Hall",
                             location: CLLocationCoordinate2DMake(43.665265, -79.391097),
                             zoom: 15.75,
                             snippet: "--"),
                
                "TH": Building(name: "Toronto School of Theology",
                             location: CLLocationCoordinate2DMake(43.664756, -79.390855),
                             zoom: 15.75,
                             snippet: "--"),
                
                "TR": Building(name: "Soldiers' Tower",
                             location: CLLocationCoordinate2DMake(43.663512, -79.39523),
                             zoom: 15.75,
                             snippet: "--"),
                
                "TT": Building(name: "455 Spadina Ave.",
                             location: CLLocationCoordinate2DMake(43.658213, -79.39989),
                             zoom: 15.75,
                             snippet: "--"),
                
                
                
                
                
                "UB": Building(name: "Upper Burwash House",
                             location: CLLocationCoordinate2DMake(43.667255, -79.391081),
                             zoom: 15.75,
                             snippet: "--"),
                
                "UC": Building(name: "University College",
                             location: CLLocationCoordinate2DMake(43.662498, -79.395477),
                             zoom: 15.75,
                             snippet: "--"),
                
                "UP": Building(name: "University College Union",
                             location: CLLocationCoordinate2DMake(43.663301, -79.397814),
                             zoom: 15.75,
                             snippet: "--"),
                
                
                
                
                
                "VA": Building(name: "Varsity Centre",
                             location: CLLocationCoordinate2DMake(43.667008, -79.397236),
                             zoom: 15.75,
                             snippet: "--"),
                
                "VC": Building(name: "Victoria College",
                             location: CLLocationCoordinate2DMake(43.666976, -79.391998),
                             zoom: 15.75,
                             snippet: "--"),
                
                "VI": Building(name: "Nona MacDonald Visitors Centre",
                             location: CLLocationCoordinate2DMake(43.661489, -79.396369),
                             zoom: 15.75,
                             snippet: "--"),
                
                "VP": Building(name: "Varsity Pavilion",
                             location: CLLocationCoordinate2DMake(43.666293, -79.396817),
                             zoom: 15.75,
                             snippet: "--"),
                
                
                
                
                
                "WA": Building(name: "123 St. George St.",
                               location: CLLocationCoordinate2DMake(43.666901, -79.39938),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WB": Building(name: "Wallberg Building",
                               location: CLLocationCoordinate2DMake(43.65904, -79.395275),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WE": Building(name: "Wetmore Hall, New College",
                               location: CLLocationCoordinate2DMake(43.662403, -79.400414),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WI": Building(name: "Wilson Hall, New College",
                               location: CLLocationCoordinate2DMake(43.661488, -79.400888),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WO": Building(name: "Woodsworth College Residence",
                               location: CLLocationCoordinate2DMake(43.667454, -79.399289),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WR": Building(name: "McCarthy House/Jackman Institute of Child Study",
                               location: CLLocationCoordinate2DMake(43.669625, -79.405952),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WS": Building(name: "Warren Stevens Building",
                               location: CLLocationCoordinate2DMake(43.663096, -79.401476),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WT": Building(name: "Whitney Hall",
                               location: CLLocationCoordinate2DMake(43.663738, -79.397978),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WW": Building(name: "Woodsworth College",
                               location: CLLocationCoordinate2DMake(43.666264, -79.399046),
                               zoom: 15.75,
                               snippet: "--"),
                
                "WY": Building(name: "Wycliffe College",
                               location: CLLocationCoordinate2DMake(43.664586, -79.395219),
                               zoom: 15.75,
                               snippet: "--"),
                
                
                
                
                
                "XG": Building(name: "665 Spadina Avenue",
                               location: CLLocationCoordinate2DMake(43.664379, -79.402342),
                               zoom: 15.75,
                               snippet: "--"),
                
                "ZC": Building(name: "88 College Street",
                               location: CLLocationCoordinate2DMake(43.660584, -79.387776),
                               zoom: 15.75,
                               snippet: "--")]



class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        GMSServices.provideAPIKey("AIzaSyAB4WOqQHLUeDDzcU-82mZyjbqUbZuB8m0")
        let camera = GMSCameraPosition.camera(withLatitude: 43.663818, longitude: -79.396578,
                                                          zoom:15.75);
        let mapView = GMSMapView.map(withFrame: CGRect.zero, camera: camera);
        view = mapView
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

