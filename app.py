"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

Multi Publish

"""

import os
import tank
from tank import TankError

class MultiPublish(tank.platform.Application):

    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        tk_multi_publish = self.import_module("tk_multi_publish")
        
        
        """
        # park this module with Nuke so that the snapshot history UI
        # pane code can find it later on.
        nuke._tk_nuke_publish = tk_nuke_publish

        # validate template_work and template_publish have the same extension
        _, work_ext = os.path.splitext(self.get_template("template_work").definition)
        _, pub_ext = os.path.splitext(self.get_template("template_publish").definition)

        if work_ext != pub_ext:
            # disable app
            self.log_error("'template_work' and 'template_publish' have different file extensions.")
            return

        # create handlers for our various commands
        self.write_node_handler = tk_nuke_publish.TankWriteNodeHandler(self)
        # immediately attach it to the nuke API so that the gizmos can reach it
        nuke._tank_write_node_handler = self.write_node_handler
        self.snapshot_handler = tk_nuke_publish.TankSnapshotHandler(self,
                                                                    self.write_node_handler)
        self.publish_handler = tk_nuke_publish.TankPublishHandler(self,
                                                                  self.snapshot_handler,
                                                                  self.write_node_handler)
        """
        
        def do_publish():
            publish_handler = tk_multi_publish.PublishHandler(self)
            publish_handler.show_dialog()
        
        # register commands:
        self.engine.register_command("Multi Publish...", do_publish)# (AD) - temp name!

        """
         # custom panes
        self.engine.register_command("Tank Snapshot History",
                                     tk_nuke_publish.snapshot_history.create_new_panel,
                                     {"type": "custom_pane",
                                      "panel_id": tk_nuke_publish.snapshot_history.PANEL_UNIQUE_ID})

        self.__add_write_nodes()
        """
        
    def destroy_app(self):
        self.log_debug("Destroying tk-multi-publish")