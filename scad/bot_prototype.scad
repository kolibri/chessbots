pcb_height = 30;
pcb_wall_width = 3;


pcb_hole_padding_w = 45.8;
pcb_hole_padding_l = 65.5;

pcb_width = pcb_hole_padding_w;
pcb_length = pcb_hole_padding_l;


pcb_screw_pin_height = 5;



pcb_hole_d = 2.7;
pcb_hole_padding_w = 45.8;
pcb_hole_padding_l = 65.5;
pcb_screw_pin_outer_d = 5;
pcb_screw_pin_inner_d = 2.7;

motorcase_hole_d = 3;
motorcase_hole_padding = 17.9;
motorcase_hole_to_axe = 19.0;
motorcase_axe_d = 7.0;
motorcase_axe_padding = 7.0;
motorcase_holder_width = 4;
motorcase_holder_height = 40;
motorcase_holder_length = 15;
wheel_d = 62;
wheel_width = 23;

bot_d = 140;
bot_base_height = 2;
fn = 32;

module bot() {
    module plate() {
        difference(){
            cylinder(h=bot_base_height, r=bot_d / 2, center=false, $fn=32);
            translate([wheel_d / 2 + motorcase_axe_padding, - wheel_d / 2, 0 ])
            cube([wheel_width, wheel_d, wheel_d]);
            translate([- wheel_d / 2 - wheel_width - motorcase_axe_padding, - wheel_d / 2, 0 ])
            cube([wheel_width, wheel_d, wheel_d]);
        }
    }

    module pcb_holder() {
        module base() {
            difference(){
                cube([pcb_width + pcb_wall_width*2, pcb_length+ pcb_wall_width*2, pcb_height]);
                translate([pcb_wall_width, pcb_wall_width, 0])
                cube([pcb_width, pcb_length, pcb_height]);

                translate([pcb_wall_width, 0, pcb_wall_width]){
                    cube([pcb_width, pcb_length+ pcb_wall_width*2, pcb_height - pcb_wall_width]);
                }

                translate([0, pcb_wall_width +10, pcb_wall_width]){
                    cube([pcb_width + pcb_wall_width*2, pcb_length - 20, pcb_height - pcb_wall_width]);
                }
                connector_screw_holes();
                //translate([0, (pcb_wall_width + 10) /2, pcb_screw_pin_height + 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
                //translate([0, pcb_length + pcb_wall_width * 2 - (pcb_wall_width + 10) /2, pcb_screw_pin_height + 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
                //translate([0, (pcb_wall_width + 10) /2, pcb_height - 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
                //translate([0, pcb_length + pcb_wall_width * 2 - (pcb_wall_width + 10) /2, pcb_height - 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
            }
            pcb_screw_pins_m(pcb_screw_pin_outer_d);
        }

        module pcb_screw_pins_m(diameter) {
            module pin() {
                cylinder(h=pcb_screw_pin_height, r=diameter / 2, center=false, $fn=fn);
            }
            translate([pcb_wall_width , pcb_wall_width, 0]) {
                pin();
                translate([pcb_hole_padding_w, 0, 0]) pin();
                translate([0, pcb_hole_padding_l, 0]) pin();
                translate([pcb_hole_padding_w, pcb_hole_padding_l, 0]) pin();
            }
        }

        difference() {
            base();
            pcb_screw_pins_m(pcb_screw_pin_inner_d);
        }
    }

    module connector_screw_holes() {
        translate([0, (pcb_wall_width + 10) /2, pcb_screw_pin_height + 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
        translate([0, pcb_length + pcb_wall_width * 2 - (pcb_wall_width + 10) /2, pcb_screw_pin_height + 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
        translate([0, (pcb_wall_width + 10) /2, pcb_height - 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
        translate([0, pcb_length + pcb_wall_width * 2 - (pcb_wall_width + 10) /2, pcb_height - 5]) rotate([0,90,0]) cylinder(h=pcb_width + pcb_wall_width*2, d=pcb_screw_pin_inner_d, center=false, $fn=fn);
    }

    
    module motor_holder(){
        //motorcase_hole_d = 3;
        //motorcase_hole_padding = 17.9;

        motor_holder_width = 3;
        motor_holder_length = pcb_hole_padding_l + pcb_wall_width*2;
        motor_holder_height = 17.9 + 5;
        total_height = 100;

        module motor_holes() {
            translate([0, motor_holder_length/2 + motorcase_hole_to_axe, motorcase_hole_d]){
                translate([0,0,0]) rotate([0,90,0]) cylinder(h=motor_holder_width, d=motorcase_hole_d, center=false, $fn=fn);
                translate([0,0,motorcase_hole_padding]) rotate([0,90,0]) cylinder(h=motor_holder_width, d=motorcase_hole_d, center=false, $fn=fn);
            }
        }

        module base() {
            cube([motor_holder_width, motor_holder_length, motor_holder_height]);
            translate([0,0,0]) cube([motor_holder_width, pcb_wall_width+10, total_height]);
            translate([0,motor_holder_length- pcb_wall_width-10,0]) cube([motor_holder_width, pcb_wall_width+10, total_height]);
        }

        module connector_holes(){
            translate([0,0 , 0]) {
            translate([0, (pcb_wall_width + 10) /2 - pcb_screw_pin_inner_d/2, 5]) cube([motor_holder_width, pcb_screw_pin_inner_d, total_height-10]);
            translate([0, pcb_length + pcb_wall_width * 2 - (pcb_wall_width + 10) /2 - pcb_screw_pin_inner_d/2, 5]) cube([motor_holder_width, pcb_screw_pin_inner_d, total_height-10]);
            }
            //cube([motor_holder_width, pcb_screw_pin_inner_d, total_height-20])
        }

        difference(){
            base();
            motor_holes();
            connector_holes();
        }

    }
    
    pcb_holder();
    //translate([-30, 0, 0]) motor_holder();
}

bot();
