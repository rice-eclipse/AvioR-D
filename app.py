import json

from flask import Flask, Response, render_template, request, jsonify
from tracking import Frame
import uuid


class App:
    def __init__(self, ip, port, detection, config):
        self.app = Flask(__name__, static_folder="website/static", template_folder="website/templates")
        self.ip = ip
        self.port = port
        self.detection = detection
        self.config = config
        self.master_uuid = None

    def start(self):
        self.__setup__()
        self.app.run(host=self.ip, port=self.port, debug=True,
                     threaded=True, use_reloader=False)

    def __setup__(self):
        app = self.app

        @app.route('/boundary_box', methods=['POST'])
        def boundary_box():
            json_data = request.get_json()
            bbox = json_data['bbox']
            # print(request.cookies.get('lock'))
            # print(self.uuid)
            if request.cookies.get('lock') == str(self.master_uuid) or self.config.website.disable_id_lock:
                self.detection.set_boundary_box(bbox)
            return {
                'response': f"{bbox} received"
            }

        @app.route("/")
        def home():
            dark_mode = False
            if request.cookies.get('dark_mode') == "true":
                dark_mode = True
            print(f"dark mode : {dark_mode}")
            return render_template("index.html",
                                   display_type=self.config.website.default_display, dark_mode=dark_mode, videos=Frame)

        @app.route('/lock_id', methods=['POST'])
        def lock():
            self.master_uuid = uuid.uuid4()
            return jsonify({"lock_id": self.master_uuid})

        @app.route('/cam_lock', methods=['POST'])
        def lock_camera():
            json_data = request.get_json()
            cam_lock = json_data['lock']
            if ((request.cookies.get('lock') == str(self.master_uuid) or self.config.website.disable_id_lock)
                    and not self.config.website.disable_cam_lock):
                self.detection.cam_lock = cam_lock
            return jsonify({"response": "success"})

        @app.route('/settings/server_config', methods=['POST'])
        def settings_send():
            return json.loads(json.dumps(self.config.website, default=lambda s: vars(s)))

        @app.route('/settings/tracking_display', methods=['POST'])
        def get_tracking_display_type():
            json_data = request.get_json()
            display = json_data['tracking_display']
            self.detection.set_tracking_display(display)
            return {
                'response': display
            }

        @app.route('/settings/display', methods=['POST'])
        def get_display_type():
            json_data = request.get_json()
            display = json_data['display']
            self.config.website.default_display = display
            return {
                'response': display
            }

        @app.route('/settings/tracking_color', methods=['POST'])
        def get_tracking_color():
            json_data = request.get_json()
            tracking_color = json_data['tracking_color']
            if request.cookies.get('lock') == str(self.master_uuid) or self.config.website.disable_id_lock:
                self.detection.set_tracking_color(tracking_color)
            return {
                'response': f"Color: {tracking_color} received."
            }

        @app.route('/settings/tracking_thickness', methods=['POST'])
        def get_tracking_thickness():
            json_data = request.get_json()
            tracking_thickness = json_data['tracking_thickness']
            if request.cookies.get('lock') == str(self.master_uuid) or self.config.website.disable_id_lock:
                self.detection.set_tracking_thickness(int(tracking_thickness))
            return {
                'response': f"Color: {tracking_thickness} received."
            }

        @app.route("/settings")
        def settings():
            dark_mode = False
            if request.cookies.get('dark_mode') == "true":
                dark_mode = True
            print(f"dark mode : {dark_mode}")
            return render_template("settings.html", dark_mode=dark_mode)

        def _gen(frame):
            print(frame)

            def _res():
                print(frame)
                return Response(self.detection.generate(frame),
                                mimetype="multipart/x-mixed-replace; boundary=frame")

            return _res

        for video in Frame:
            print(video)

            app.add_url_rule(video.url, video.label, _gen(video))
