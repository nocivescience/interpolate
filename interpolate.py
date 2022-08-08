from turtle import circle
from unittest import result
from manim import *
class InpterpolateScene(ThreeDScene):
    CONFIG={
        'n_circles':12
    }
    def construct(self):
        axes=ThreeDAxes()
        axes.set_stroke(width=1)
        self.move_camera(phi=70*DEGREES,theta=-145*DEGREES,run_time=1)
        self.begin_ambient_camera_rotation()
        short_circles=self.get_cylinder_circles(2,.05,.5)
        tall_circles=short_circles.copy().scale(0.125)
        torus_circles=tall_circles.copy()
        for circle in torus_circles:
            circle.shift(RIGHT)
            z=circle.get_center()[2]
            circle.shift(z*IN)
            angle=PI*z/2
            circle.rotate(angle,axis=DOWN,about_point=ORIGIN)
        circles=short_circles.copy()
        flow_lines=self.get_flow_lines(circles)
        self.add(axes)
        self.play(Transform(circles,tall_circles))
        self.play(Transform(circles,torus_circles))
        self.wait()
    def get_cylinder_circles(self,radius,radius_var,max_z):
        return VGroup(*[
            ParametricFunction(
                lambda t: np.array([
                    np.cos(TAU*t)*r,
                    np.sin(TAU*t)*r,
                    z
                ]),**self.get_circle_kwargs()
            )
            for z in sorted(max_z*np.random.random(self.CONFIG['n_circles']))
            for r in [radius+radius_var*np.random.random()]
        ]).center()
    def get_circle_kwargs(self):
        return {
            'stroke_color':BLACK,
            'stroke_width': 0,
        }
    def get_torus_circles(self,out_r,in_r,r_var):
        result=VGroup()
        for u in sorted(np.random.random(self.CONFIG['n_circles'])):
            r=in_r+r_var*np.random.random()
            circle=ParametricFunction(
                lambda t: np.array([
                    np.cos(TAU*t),
                    np.sin(TAU*t),
                    0
                ]), **self.get_circle_kwargs()
            )
            circle.shift(out_r*RIGHT)
            circle.rotate(
                TAU*u-PI,about_point=ORIGIN,axis=DOWN
            )
            result.add(circle)
        return result
    def get_flow_lines(self,circle_group):
        window=0.3
        def update_circle(self,dt):
            circle.total_time+=dt
            diameter=np.linalg.norm(
                circle.template.point_from_proportion(0),
                circle.template.point_from_proportion(.6)
            )
            modulus=np.sqrt(diameter)+.1
            alpha=(circle.total_time%modulus)/modulus
            circle.pointwise_become_partial(
                circle.template,
                max(interpolate(-window,1,alpha),0),
                min(interpolate(0,1+window,alpha),1)
            )
        result=VGroup()
        for template in circle_group:
            circle=template.copy()
            circle.set_stroke(color=interpolate_color(BLUE_A,BLUE_E,np.random.random()))
            circle.template=template
            circle.total_time=4*np.random.random()
            circle.add_updater(update_circle)
            result.add(circle)
        return result