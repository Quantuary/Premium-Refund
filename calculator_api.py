#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:26:00 2020

@author: marcus
"""

from flask_restful import Resource, Api
api = Api(app)


class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)

        output = prediction[0]
        return jsonify({'Result':output})


api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(debug=True)
