# Copyright 2013 Devsim LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

####
#### cap2.py
#### tests physics of cap made of two insulating regions
####
from ds import *
device="MyDevice"
interface="MySiOx"
regions =("MyOxRegion", "MySiRegion")

create_1d_mesh(mesh="cap")
add_1d_mesh_line(mesh="cap", pos=0,   ps=0.1, tag="top")
add_1d_mesh_line(mesh="cap", pos=0.5, ps=0.1, tag="mid")
add_1d_mesh_line(mesh="cap", pos=1,   ps=0.1, tag="bot")
add_1d_contact  (mesh="cap", name="top",    tag="top", material="metal")
add_1d_contact  (mesh="cap", name="bot",    tag="bot", material="metal")
add_1d_interface(mesh="cap", name="MySiOx", tag="mid")
add_1d_region   (mesh="cap", material="Si", region="MySiRegion", tag1="top", tag2="mid")
add_1d_region   (mesh="cap", material="Ox", region="MyOxRegion", tag1="mid", tag2="bot")
finalize_mesh(mesh="cap")
create_device(mesh="cap", device=device)

set_parameter(device=device, region="MySiRegion", name="Permittivity", value=11.1*8.85e-14)
set_parameter(device=device, region="MySiRegion", name="ElectricCharge", value=1.6e-19)

set_parameter(device=device, region="MyOxRegion", name="Permittivity", value=3.9*8.85e-14)

set_parameter(device=device, region="MyOxRegion", name="ElectricCharge", value=1.6e-19)

for region in regions:
  node_solution(device=device, region=region, name="Potential")
  edge_from_node_model(device=device, region=region, node_model="Potential")

  edge_model(device=device, region=region, name="ElectricField",
                   equation="(Potential@n0 - Potential@n1)*EdgeInverseLength")

  edge_model(device=device, region=region, name="ElectricField:Potential@n0",
                   equation="EdgeInverseLength")

  edge_model(device=device, region=region, name="ElectricField:Potential@n1",
                   equation="-EdgeInverseLength")

  edge_model(device=device, region=region, name="PotentialEdgeFlux", equation="Permittivity*ElectricField")
  edge_model(device=device, region=region, name="PotentialEdgeFlux:Potential@n0", equation="diff(Permittivity*ElectricField, Potential@n0)")
  edge_model(device=device, region=region, name="PotentialEdgeFlux:Potential@n1", equation="-PotentialEdgeFlux:Potential@n0")

  equation(device=device, region=region, name="PotentialEquation", variable_name="Potential", node_model="",
      edge_model="PotentialEdgeFlux", time_node_model="", variable_update="default") 

set_parameter(device=device, region="MySiRegion", name="topbias"   , value=1.0)
set_parameter(device=device, region="MyOxRegion", name="bottombias", value=0.0)


conteq="Permittivity*ElectricField"

node_model(device=device, region="MySiRegion", name="topnode_model",           equation="Potential - topbias")
node_model(device=device, region="MySiRegion", name="topnode_model:Potential", equation="1")
edge_model(device=device, region="MySiRegion", name="contactcharge_edge_top",  equation=conteq)

node_model(device=device, region="MyOxRegion", name="bottomnode_model",           equation="Potential - bottombias")
node_model(device=device, region="MyOxRegion", name="bottomnode_model:Potential", equation="1")
edge_model(device=device, region="MyOxRegion", name="contactcharge_edge_bottom",  equation=conteq)

contact_equation(device=device, contact="top", name="PotentialEquation", variable_name="Potential",
			node_model="topnode_model", edge_model="",
			node_charge_model="", edge_charge_model="contactcharge_edge_top",
			node_current_model="",   edge_current_model="")

contact_equation(device=device, contact="bot", name="PotentialEquation", variable_name="Potential",
			node_model="bottomnode_model", edge_model="",
			node_charge_model="", edge_charge_model="contactcharge_edge_bottom",
			node_current_model="", edge_current_model="")

# type continuous means that regular equations in both regions are swapped into the primary region
interface_model(device=device, interface=interface, name="continuousPotential", equation="Potential@r0-Potential@r1")
interface_model(device=device, interface=interface, name="continuousPotential:Potential@r0", equation= "1")
interface_model(device=device, interface=interface, name="continuousPotential:Potential@r1", equation="-1")
interface_equation(device=device, interface=interface, name="PotentialEquation", variable_name="Potential", interface_model="continuousPotential", type="continuous")



solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

print(get_contact_charge(device=device, contact="top", equation="PotentialEquation"))
print(get_contact_charge(device=device, contact="bot", equation="PotentialEquation"))

print_edge_values(device=device, region="MySiRegion", name="PotentialEdgeFlux")
print_edge_values(device=device, region="MyOxRegion", name="PotentialEdgeFlux")
set_parameter(device=device, region="MySiRegion", name="Permittivity", value=1.0*8.85e-14)
set_parameter(device=device, region="MyOxRegion", name="Permittivity", value=1.0*8.85e-14)
print_edge_values(device=device, region="MySiRegion", name="PotentialEdgeFlux")
print_edge_values(device=device, region="MyOxRegion", name="PotentialEdgeFlux")

solve(type="dc", absolute_error=1.0, relative_error=1e-14, maximum_iterations=30)
print_edge_values(device=device, region="MySiRegion", name="PotentialEdgeFlux")
print_edge_values(device=device, region="MyOxRegion", name="PotentialEdgeFlux")
print(get_contact_charge(device=device, contact="top", equation="PotentialEquation"))
print(get_contact_charge(device=device, contact="bot", equation="PotentialEquation"))

set_parameter(device=device, name="Permittivity", value=11.1*8.85e-14)
set_parameter(device=device, region="MySiRegion", name="Permittivity", value=11.1*8.85e-14)
set_parameter(device=device, region="MyOxRegion", name="Permittivity", value=3.9*8.85e-14)

solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)
print_edge_values(device=device, region="MySiRegion", name="PotentialEdgeFlux")
print_edge_values(device=device, region="MyOxRegion", name="PotentialEdgeFlux")
print_edge_values(device=device, region="MySiRegion", name="ElectricField")
print_edge_values(device=device, region="MyOxRegion", name="ElectricField")
print_node_values(device=device, region="MySiRegion", name="Potential")
print_node_values(device=device, region="MyOxRegion", name="Potential")
print (get_contact_charge(device=device, contact="top", equation="PotentialEquation"))
print (get_contact_charge(device=device, contact="bot", equation="PotentialEquation"))


