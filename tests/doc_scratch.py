xxx = {
  "_id": "NUMENOR.assets.characters.hulk",
  "entry_name": "hulk",
  "type": "asset",
  "status": "",
  "active": true,
  "origin_db_path": "NUMENOR.assets.characters",
  "assignment": {},
  "assigned_to": [],
  "definition": {
    "asset_lod": "hero",
    "assembly": false,
    "full_range_in": "1001",
    "full_range_out": "1100",
    "frame_in": "1001",
    "frame_out": "1001",
    "handles_head": "8",
    "handles_tail": "8",
    "preroll": "10",
    "shot_type": "vfx",
    "cut_in": "1009",
    "cut_out": "993",
    "frame_rate": "24",
    "motion_blur_high": "0.25",
    "motion_blur_low": "-0.25",
    "res_x": "from plate",
    "res_y": "from plate"
  },
  "tasks": {
    "cfx_set": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "groom": {},
        "modeling": {}
      },
      "pub_slots": {
        "cloth_setup": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "scn",
          "used_by": []
        },
        "feathers_setup": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "scn",
          "used_by": []
        },
        "fur_setup": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "scn",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "concept": {
      "active": true,
      "artist": "None",
      "imports_from": {},
      "pub_slots": {
        "img": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": [
            "modeling"
          ]
        },
        "pdf": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "scn",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "facs": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "modeling": {},
        "texturing": {}
      },
      "pub_slots": {
        "corrective": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": [
            "rigging"
          ]
        },
        "main_shapes": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": [
            "rigging"
          ]
        }
      },
      "status": "NOT-STARTED"
    },
    "fx_set": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "modeling": {}
      },
      "pub_slots": {
        "bgeo": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": []
        },
        "vdb": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "csh",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "groom": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "modeling": {},
        "texturing": {}
      },
      "pub_slots": {
        "groom_set": {
          "active": true,
          "method": "scn_exp",
          "reviewable": true,
          "source": {},
          "type": "csh",
          "used_by": [
            "cfx_set"
          ]
        },
        "guides": {
          "active": true,
          "method": "scn_exp",
          "reviewable": "False",
          "source": {},
          "type": "csh",
          "used_by": [
            "cfx_set"
          ]
        }
      },
      "status": "NOT-STARTED"
    },
    "lidar": {
      "active": true,
      "artist": "None",
      "imports_from": {},
      "pub_slots": {
        "img": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": [
            "modeling"
          ]
        },
        "pdf": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "scn",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "modeling": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "concept": {},
        "sculpting": {}
      },
      "pub_slots": {
        "ao_map": {
          "active": true,
          "method": "geo_bake",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        },
        "curvature_map": {
          "active": true,
          "method": "geo_bake",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        },
        "lidar": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": []
        },
        "proj_geo": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": []
        },
        "proxy_geo": {
          "active": true,
          "method": "sf_csh",
          "reviewable": true,
          "source": {},
          "type": "geo",
          "used_by": [
            "rigging",
            "cfx_set"
          ]
        },
        "rend_geo": {
          "active": true,
          "method": "sf_csh",
          "reviewable": true,
          "source": {},
          "type": "geo",
          "used_by": [
            "rigging",
            "cfx_set",
            "groom"
          ]
        },
        "selection_map": {
          "active": true,
          "method": "geo_bake",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        },
        "tex_object": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": []
        },
        "utility": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": [
            "rigging",
            "cfx_set"
          ]
        },
        "vport_mat": {
          "active": true,
          "method": "assign_exp",
          "reviewable": false,
          "source": {},
          "type": "scn",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "rigging": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "facs": {},
        "modeling": {}
      },
      "pub_slots": {
        "cmuscle_rig": {
          "active": true,
          "method": "scn_exp",
          "reviewable": true,
          "source": {},
          "type": "scn",
          "used_by": []
        },
        "proxy_rig": {
          "active": true,
          "method": "scn_exp",
          "reviewable": true,
          "source": {},
          "type": "scn",
          "used_by": []
        },
        "render_rig": {
          "active": true,
          "method": "scn_exp",
          "reviewable": true,
          "source": {},
          "type": "scn",
          "used_by": []
        },
        "util_rig": {
          "active": true,
          "method": "scn_exp",
          "reviewable": false,
          "source": {},
          "type": "scn",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "sculpting": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "concept": {}
      },
      "pub_slots": {
        "cavity": {
          "active": true,
          "method": "geo_bake",
          "reviewable": false,
          "source": {},
          "type": "img",
          "used_by": [
            "texturing",
            "surfacing"
          ]
        },
        "displ": {
          "active": true,
          "method": "geo_bake",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": [
            "texturing",
            "surfacing"
          ]
        },
        "normal": {
          "active": true,
          "method": "geo_bake",
          "reviewable": false,
          "source": {},
          "type": "img",
          "used_by": [
            "texturing",
            "surfacing"
          ]
        },
        "ref_geo": {
          "active": true,
          "method": "sf_csh",
          "reviewable": false,
          "source": {},
          "type": "geo",
          "used_by": [
            "modeling",
            "surfacing"
          ]
        }
      },
      "status": "NOT-STARTED"
    },
    "surfacing": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "modeling": {},
        "sculpting": {},
        "texturing": {}
      },
      "pub_slots": {
        "look_dev": {
          "active": true,
          "method": "scn_exp",
          "reviewable": true,
          "source": {},
          "type": "cfg",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    },
    "texturing": {
      "active": true,
      "artist": "None",
      "imports_from": {
        "modeling": {}
      },
      "pub_slots": {
        "groom_maps": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": [
            "groom"
          ]
        },
        "texture_set": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        },
        "util_maps": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        },
        "vport_tex": {
          "active": true,
          "method": "img_exp",
          "reviewable": true,
          "source": {},
          "type": "img",
          "used_by": []
        }
      },
      "status": "NOT-STARTED"
    }
  },
  "components": {},
  "config": {},
  "data": {
    "stack_streams": [
      "main",
      "customA",
      "customB"
    ],
    "variant_sets": {
      "geo_var_sets": {
        "geo_var_set__A": [
          "varNameX",
          "varNameY"
        ],
        "geo_var_set__B": [
          "varNameX",
          "varNameY"
        ]
      },
      "groom_var_sets": {},
      "mtl_var_sets": {
        "mtl_var_set__A": [
          "varNameX",
          "varNameY"
        ]
      }
    }
  },
  "children": [],
  "visual_children": [],
  "parent": "NUMENOR",
  "visual_parent": "NUMENOR.assets.characters",
  "date": "2024-03-07",
  "time": "20:20",
  "owner": "arsithra"
}