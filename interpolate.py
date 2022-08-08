from turtle import circle
from manim import *
class InpterpolateScene(Scene):
    CONFIG={
        'n_circles':12
    }
    def construct(self):
        circles=VGroup()
        for t in range(7):
            t=np.random.random()+1
            circle=Circle(radius=t)
            circle.set_stroke(RED,opacity=0.2)
            circles.add(circle)
        flow_lines=self.get_flow_lines(circles)
        self.add(circles,flow_lines)
        self.wait(26)
    def get_flow_lines(self,circle_group):
        window=.03
        def update_circle(circle,dt):
            circle.total_time+=dt
            diameter=4
            alpha=(
                circle.total_time%diameter
            )/diameter
            circle.pointwise_become_partial(
                circle.template,
                max(interpolate(-window,1,alpha),0),
                min(interpolate(0,1+window,alpha),1)
            )
        result=VGroup()
        for template in circle_group:
            circle=template.copy()
            circle.set_stroke(
                color=interpolate_color(
                    BLUE_A,BLUE_E,np.random.random()
                )
            )
            circle.template=template
            circle.total_time=3*np.random.random()
            circle.add_updater(update_circle)
            result.add(circle)
        return result