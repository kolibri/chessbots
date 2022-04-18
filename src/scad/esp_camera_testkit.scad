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

esp_mock();
