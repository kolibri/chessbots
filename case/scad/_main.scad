include <bot_prototype.scad>
//include <esp_camera_testkit.scad>


//show_espcam_testkit = false;
show_bot_prototype = false;
show_bot_prototype_print = false;
show_bot_prototype_tests = true;

//if (true == show_espcam_testkit) {
//    top();
//    bottom();
//}

if (true == show_bot_prototype) {
    bot_prototype();
}

if (true == show_bot_prototype_print) {
    bot_prototype_print();
}

if (true == show_bot_prototype_tests) {
    bot_prototype_tests();
}
