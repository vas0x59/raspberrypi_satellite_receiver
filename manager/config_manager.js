const fs = require("fs")

function satellites_d_to_l(sats) {
    let satellites_list = []
    for (let key in sats) {
        if (sats.hasOwnProperty(key)) {
            let el = sats[key]
            el.name = key
            satellites_list.push(el)
        }
    }
    return satellites_list
}
function ungroup_satellites(sats_g) {
    let sats_ug = {}
    for (let key_t in sats_g) {
        let el_t = sats_g[key_t]
        for (let key_s in el_t){
            let el_s = el_t[key_s]
            el_s["type"] = key_t
            sats_ug[key_s] = el_s
        }
    }
    return sats_ug
}


class ConfigManager {
    constructor(configs_path) {
        this.configs_path = configs_path
        this.receivers_configs = {}
        this.load_main()
        this.load_all_sats_type_configs()
    }
    load_main() {
        this.main_config = JSON.parse(fs.readFileSync(this.configs_path + "/main_config.json").toString())
        console.log(this.main_config)
        console.log(satellites_d_to_l(ungroup_satellites(this.main_config["satellites"])))
    }
    save_main() {
        fs.writeFileSync(this.configs_path + "/main_config.json", JSON.stringify(this.main_config))
    }
    load_all_sats_type_configs() {
        let list_of_sats = satellites_d_to_l(ungroup_satellites(this.get_main("satellites")))
        for (let key in list_of_sats) {
            let el = list_of_sats[key]
            let path_to_config = this.configs_path + "/satellites/" + el["type"] + "/receiver.json"
            this.receivers_configs[el["type"]] = JSON.parse(fs.readFileSync(path_to_config).toString())
        }
    }
    save_receiver(type){
        let path_to_config = this.configs_path + "/satellites/" + type + "/receiver.json"
        fs.writeFileSync(path_to_config, JSON.stringify(this.receivers_configs[type]))
    }

    get_main(field) {
        return this.main_config[field]
    }
    set_main(field, value) {
        this.main_config[field] = value
        this.save_main()
    }
    get_receiver(type, field) {
        return this.receivers_configs[type][field]
    }
    set_receiver(type, field, value) {
        this.receivers_configs[type][field] = value
        this.save_receiver(type)
    }
}

module.exports.ConfigManager = ConfigManager
module.exports.satellites_d_to_l = satellites_d_to_l
module.exports.ungroup_satellites = ungroup_satellites