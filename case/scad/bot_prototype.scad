m3_d = 2.7;
base_square_size = 100;
motorcase_hole_padding = 17.9;
connector_length = 15;
wall_strength = 5;

module hole_pair(fn=8, padding, diameter, height) {
    rotate([90,0,0]) cylinder(h=height, d=diameter, center=false, $fn=fn);
    translate([0,0,padding]) rotate([90,0,0]) cylinder(h=height, d=diameter, center=false, $fn=fn);
}

module part_bottom_case(fn=8) {
    base_height = 10;
    hole_d = m3_d;
    motor_holder_height = 23;
    
    module raw() {
        cube([
            base_square_size,
            base_square_size,
            base_height
        ]);
        translate([base_square_size/2 - connector_length/2,0,0]){
            cube([connector_length, 
                wall_strength, 
                motor_holder_height
            ]);
        }

        translate([base_square_size/2 - connector_length/2,base_square_size - wall_strength,0]){
            cube([connector_length, 
                wall_strength, 
                motor_holder_height
            ]);
        }

    }

    difference() {
        raw();
        translate([wall_strength, wall_strength, 0]) {
            cube([
                base_square_size - wall_strength * 2,
                base_square_size - wall_strength * 2,
                base_height
            ]);
        }

        translate([base_square_size/2,wall_strength, hole_d])
        hole_pair(fn, motorcase_hole_padding, hole_d, wall_strength);
        translate([base_square_size/2,base_square_size,hole_d])
        hole_pair(fn, motorcase_hole_padding, hole_d, wall_strength);
    }
}

module part_pcb_case(fn=8) {
    pcb_mount_d = 2.7;
    hth_x = 65.5;
    hth_y = 45.5;
    base_height = 2;
    case_holder_height = 25;
    case_hole_padding = 20;
    case_connector_d = m3_d;

    module raw(){
        translate([0,base_square_size/2 - hth_y/2 - pcb_mount_d,0]){
            cube([
                hth_x + pcb_mount_d*2, hth_y + pcb_mount_d*2, base_height
            ]);
        }

        cube([hth_x+pcb_mount_d*2, base_square_size, base_height]);

        translate([base_square_size/2 - connector_length/2,0,0]){
            cube([connector_length, 
                wall_strength, 
                case_holder_height
            ]);
        }

        translate([base_square_size/2 - connector_length/2,base_square_size - wall_strength,0]){
            cube([connector_length, 
                wall_strength, 
                case_holder_height
            ]);
        }
    }

    difference() {
        raw();
        translate([pcb_mount_d*2,wall_strength ,0])
            cube([hth_x-pcb_mount_d*2, base_square_size - wall_strength*2, base_height]);

        translate([pcb_mount_d,base_square_size/2 - hth_y/2 ,0]){
            cylinder(h=base_height, d=pcb_mount_d, center=false, $fn=fn);
            translate([hth_x,0,0])
            cylinder(h=base_height, d=pcb_mount_d, center=false, $fn=fn);
            translate([0,hth_y,0])
            cylinder(h=base_height, d=pcb_mount_d, center=false, $fn=fn);
            translate([hth_x,hth_y,0])
            cylinder(h=base_height, d=pcb_mount_d, center=false, $fn=fn);
        }
        translate([base_square_size/2,wall_strength,(case_holder_height - case_hole_padding)/2])
            hole_pair(fn, case_hole_padding, case_connector_d, wall_strength);
        translate([base_square_size/2,base_square_size,(case_holder_height - case_hole_padding)/2])
            hole_pair(fn, case_hole_padding, case_connector_d, wall_strength);
    }
}

module part_connector(fn=8, strength=3, width=15, length=100, diameter=2.7) {
    difference() {
        cube([width, strength, length]);
        
        translate([width/2 - diameter/2, 0, 23])
        cube([diameter, strength, length - diameter*2-23]);
        
        translate([width/2, strength, diameter])
        hole_pair(fn, motorcase_hole_padding, diameter, strength);
    }
}

module bot_prototype() {
    part_bottom_case(8);

    translate([0,base_square_size,50])
    rotate([180, 0, 0])
    part_pcb_case(8);

    translate([base_square_size/2-15/2,5,0])
    part_connector(8);
    translate([base_square_size/2-15/2,base_square_size-5-3,0])
    part_connector(8);
}

module bot_prototype_print() {
    translate([base_square_size *1.1,0,0])
    part_pcb_case(32);
    
    translate([0,base_square_size *1.1,0])
    part_bottom_case(32);

    translate([base_square_size *1.1,base_square_size *1.1*2,0])
    rotate([90, 0,0])
    part_connector(32);

    translate([base_square_size *1.1 + 30,base_square_size *1.1*2,0])
    rotate([90, 0,0])
    part_connector(32);
}

module bot_prototype_tests() {
    width = 7;
    strength = 3;
    length = 23;
    diameter = m3_d;

    rotate([90,0,0])
    difference() {
        cube([width, strength, length]);
        
        translate([width/2 - diameter/2, 0, 23])
        cube([diameter, strength, length - diameter*2-23]);
        
        translate([width/2, strength, diameter])
        hole_pair(32, motorcase_hole_padding, diameter, strength);
    }

    translate([15,-length,width])
    rotate([0,90, 90])
    difference() {
        cube([width, strength, length]);

        translate([width/2 - diameter/2, 0, 23])
        cube([diameter, strength, length - diameter*2-23]);
        
        translate([width/2, strength, diameter])
        hole_pair(32, motorcase_hole_padding, diameter, strength);
    }
}
