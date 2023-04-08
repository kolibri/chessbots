esp_height=19;
esp_width=27;
esp_length=40;
esp_upper_pin_height=5;
esp_upper_pin_length=24;
esp_upper_pin_width=2.6;
esp_upper_pin_margin_x=0.8;
esp_upper_pin_margin_y=3.4;
esp_middle_height=7;
esp_camara_margin_y=5.4;
esp_camara_margin_x=9.6;
esp_camara_width=8.7;
esp_camara_length=8.7;

//esp_camara_heigt = esp_height - esp_upper_pin_height - esp_middle_height; // = 19-5-7 = 7
esp_camara_heigt = 6.3;


bottom_plate_height=1.5;
bottom_plate_width=27;
bottom_plate_length=40;

bottom_height=1.5;
bottom_width=27;
bottom_length=60;


screw_m3_d = 3.03 / 2;
screw_fn = 32;

lego_1=7.8;
lego_stud_height=1.9;
lego_stud_margin=1;


module esp_mock(){

    // pin rows
    translate([esp_upper_pin_margin_x, 0, esp_height - esp_upper_pin_height])
    cube([esp_upper_pin_width, esp_upper_pin_length, esp_upper_pin_height]);
    translate([esp_width - esp_upper_pin_width - esp_upper_pin_margin_x, 0, esp_height - esp_upper_pin_height])
    cube([esp_upper_pin_width, esp_upper_pin_length, esp_upper_pin_height]);

    // main body
    translate([0,0,esp_height - esp_upper_pin_height - esp_middle_height])
    cube([esp_width,esp_length,esp_middle_height]);

    // camera
    translate([esp_camara_margin_x,esp_camara_margin_y,0])
    cube([esp_camara_width,esp_camara_length,esp_height - esp_upper_pin_height - esp_middle_height]);
}


module bottom() {
    module bottom_stand() {


        difference(){
            cube([bottom_plate_width, bottom_plate_length, bottom_plate_height]);
        }

        translate([esp_camara_margin_x-1,esp_camara_margin_y-1,bottom_plate_height]){
            difference(){
                cube([esp_camara_width+2,esp_camara_length+2,0.5]);
                translate([1,1,0])
                cube([esp_camara_width,esp_camara_length,0.5]);
            }
        }

        translate([esp_camara_margin_x-(0.75+3),0,bottom_plate_height])
        cube([3,bottom_plate_length,esp_camara_heigt]);

        translate([esp_camara_margin_x+esp_camara_width + (0.75),0,bottom_plate_height])
        cube([3,bottom_plate_length,esp_camara_heigt]);
    }

    module bottom_rest() {
        translate([0,-10,0])
        cube([bottom_width,bottom_length+3,bottom_height]);


        translate([0,-5,bottom_height]){
            difference(){

                cube([bottom_width,5,esp_camara_heigt+esp_middle_height]);
                translate([bottom_width/2, 2.5, 0])
                cylinder(h=esp_middle_height+esp_camara_heigt, r=screw_m3_d, center=false, $fn=20);
            }

        }

        translate([0,bottom_plate_length,bottom_height]){
            difference(){

                cube([bottom_width,5,esp_camara_heigt+esp_middle_height]);
                translate([bottom_width/2, 2.5, 0])
                cylinder(h=esp_middle_height+esp_camara_heigt, r=screw_m3_d, center=false, $fn=20);
            }
        }

    }

    module lego_holder(){

        difference(){

            cube([4*lego_1,2*lego_1,lego_stud_height]);

            translate([lego_stud_margin, lego_stud_margin, 0])
            cube([4*lego_1 - lego_stud_margin*2,2*lego_1 - lego_stud_margin*2,lego_stud_height]);
        }


    }

    difference(){
        bottom_rest();
        translate([esp_camara_margin_x+esp_camara_length/2, esp_camara_margin_y+esp_camara_length/2, 0])
        cylinder(h=bottom_plate_height+100, r=esp_camara_length/2-1,center=false,$fn=16);
    }
    difference(){
        bottom_stand();
        translate([esp_camara_margin_x+esp_camara_length/2, esp_camara_margin_y+esp_camara_length/2, 0])
        cylinder(h=bottom_plate_height+100, r=esp_camara_length/2-1,center=false,$fn=16);
    }

    translate([(lego_1*4 - bottom_width)/-2, -10-lego_1*2, 0])
    lego_holder();
    translate([(lego_1*4 - bottom_width)/-2, -10-lego_1*2 + lego_1*10, 0])
    lego_holder();
}

module top(){
    difference(){
        translate([(bottom_width-18)/2,-5,0])
        cube([18,esp_length+10,3]);

        translate([(bottom_width)/2,-2.5,0])
        cylinder(h=3, r=screw_m3_d, $fn=20);
        translate([(bottom_width)/2,bottom_plate_length+2.5,0])
        cylinder(h=3, r=screw_m3_d, $fn=20);


    }


}

/*
module base_body(){
    difference(){
        cube([
            screw_extension_width*2 + wall_strength*2 + base_width,
            base_depth,
            base_height + wall_strength*2
        ]);
        
        translate([screw_extension_width + wall_strength, 0, wall_strength]) cube([base_width, base_depth, base_height+wall_strength]);
        cube([screw_extension_width, base_depth, base_height+wall_strength]);
        translate([screw_extension_width + wall_strength*2 + base_width, 0, 0]) cube([screw_extension_width, base_depth, base_height+wall_strength]);
    }
}
*/
//translate([0,0,bottom_plate_height])
//esp_mock();



//translate([0,0,bottom_height+esp_camara_heigt+esp_middle_height])
//top();
//bottom();