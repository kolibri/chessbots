fn=64;

module motor_mount_holes(){
    cube([2.9,11.3,3]);
    translate([18.8+2.9,0,0])
    cube([2.8,11.3,3]);
}
module motors(){
    translate([2,2,0])
    motor_mount_holes();
    
    mirror([])
    translate([-98,2,0])
    motor_mount_holes();
} 

module esp_mount(){
    module hole_mount(){
        difference(){
            cylinder(d=5,h=14,$fn=fn);
            cylinder(d=2.6,h=14,$fn=fn);
        }
    }
    // 33.02
    // 27.94
    translate([-33.02/2,-27.94/2,0]){
        hole_mount();
        translate([0,27.94,0])    
        hole_mount();
        translate([33.02,0,0])    
        hole_mount();
        translate([33.02,27.94,0])    
        hole_mount();
    }
}
module voltdowner_mount(){
    module hole_mount(){
        difference(){
            cylinder(d=5,h=5,$fn=fn);
            cylinder(d=2.6,h=5,$fn=fn);
        }
    }
    // 33.02
    // 27.94
    translate([-15,16,0]){
        hole_mount();
        translate([30,-16,0])    
        hole_mount();
    }
}



module bat_mount(){
// 58  47
    translate([-61/2,0,0]){
        difference(){
            cube([61,50,5]);
            
            translate([1.5,1.5,0])
            cube([58,47,5]);

            translate([11.5,0,0])
            cube([38,51,5]);

            translate([0,11.5,0])
            cube([62,27,5]);
        }
    }
}





difference(){
    cube([100,150,3]);
    motors();

    translate([50-27/2,5,0])
    cube([27,40,3]);
    
    
    translate([50,145,0])
    cylinder(h=3, d=5,$fn=fn);
}

translate([0,0,3]){
    translate([50,20,0])
    esp_mount();

    translate([50,60,0])
    bat_mount();

    translate([50,120,0])
    voltdowner_mount();

    

    translate([50,145,0])
    difference(){
        cylinder(d=7,h=10,$fn=fn);
        cylinder(d=5,h=10,$fn=fn);
    }

}