type atree = (tree, int)
type tree = Leaf | Node of char * (atree list)

let group (xs: 'a list) (hash: 'a -> 'b) : ('a list) list =
  match xs with
  | [] -> [[]]
  | x::tl ->
    let x_id = hash x in
    let x_group = List.partition (fun y -> hash y = x_id) tl in
    (x_id, x::x_group) @ group tl hash

let build_atree (ss: string list) : atree =
  let empty, nonempty = partition (fun s -> String.length s = 0) ss in
  let empty_list : atree list = map (fun _ -> (Leaf, 1)) empty in
  let groups = group ss (fun s -> String.get s 0) nonempty in
