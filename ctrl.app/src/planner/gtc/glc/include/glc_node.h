/* Copyright (C) Brian Paden (bapaden@mit.edu)
 * Written by Brian Paden
 * Released under the MIT License
 */

#ifndef GLC_UTILS_H
#define GLC_UTILS_H

#include <memory>
#include <chrono>
#include <random>
#include <queue>
#include <deque>
#include <valarray>
#include <algorithm> 

#include "glc_interpolation.h"

namespace glc{
  
  /**
   * \brief Node object used in motion planning search tree
   * 
   * The Node object in the glc library will always belong to a motion 
   * planning search tree. Each Node contains pointers to its parent
   * and children in the tree. A Node is also associated to a state in 
   * the state space as well as a cost to reach that Node via the path
   * from the root of the tree. The node also has an attribute "merit"
   * which is the cost from the root together with the estimated 
   * cost-to-go which is used in the A*-like search. 
   */
  struct Node{
    //! \brief The pointer to this node's parent
    std::shared_ptr<const Node> parent;
    //! \brief The trajectory from the parent node to this node
    std::shared_ptr<InterpolatingPolynomial> trajectory_from_parent;
    //! \brief The control signal producing the trajectory from the parent node to this node
    std::shared_ptr<InterpolatingPolynomial> control_from_parent;
    //! \brief An array of pointers to this node's children
//     std::vector< std::shared_ptr<const Node> > children;
    //! \brief The state or configuration associated with this node
    std::valarray<double> state;
    //! \brief The duration of a trajectory from the root of the search tree to the state of this node
    double time=0;
    //! \brief The cost to reach this node from the root
    double cost=0;
    //! \brief The cost together with the estimated cost-to-go which is used for an informed search
    double merit=0;
    //! \brief The index from the discrete control set used to reach this node from the parent in the current instance of the algorithm
    int u_idx=0;
    //! \brief The depth of this node in the search tree
    int depth=0;
    //! \brief A flag to indicate if this Node is in the goal set
    bool in_goal = false;
    
    /**
     * \brief Constructor for the Node object which sets several of the struct's attributes
     * \param[in][in] card_omega_ is the cardinality of the discrete set of controls used in this instance of the algorithm
     * \param[in] control_index_ is the index of the control used to reach this node's state from the its parent
     * \param[in] cost_ is the cost to reach this node from the root
     * \param[in] cost_to_go_ is an underestimate of the remaining cost-to-go from the state of this node
     * \param[in] state_ is a the state of the system associated with this Node
     * \param[in] time_ is the duration of the trajectory from the root to this node in the search tree
     * \param[in] parent_ is a pointer to the parent of this Node
     */
    Node(int _card_omega, 
               int _control_index, 
               double _cost, 
               double _cost_to_go, 
               const std::valarray<double>& _state, 
               double _time,
               const std::shared_ptr<const Node> _parent,
               const std::shared_ptr<InterpolatingPolynomial>& _trajectory_from_parent,
               const std::shared_ptr<InterpolatingPolynomial>& _control_from_parent);
  };
  
  /**
   * \brief A structure for defining a weak linear ordering of nodes based on the ordering of their merit attribute.
   *
   * This ordering is used to order a priority queue used in the A* like search. 
   */
  struct NodeMeritOrder{
  public:
    /**
     * \brief The function defining the "less than" relation between two nodes
     * \param[in] node1 is the left element to be checked for membership in the relation
     * \param[in] node2 is the right element to be checked for membership in the relation
     * \returns true if the merit of node1 is less than the merit of node2 and false otherwise.
     */ 
    bool operator()(const std::shared_ptr<const Node>& node1, const std::shared_ptr<const Node>& node2);
  };
  
}//namespace glc
#endif
