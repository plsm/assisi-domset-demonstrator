library ("data.table")
library ("ggplot2")


analysis <- fread ("analysis.csv")

read.repeat.data <- function (
  filename
) {
  cat (sprintf ("Reading %s\n", filename))
  result <- fread (
      input = filename,
      col.names = c (
          "time",
          "run",
          "criterion",
          "max.depth",
          "min.samples.split",
          "random.chance.winscore",
          "success.rate",
          "false.positive",
          "false.negative"
      )
  )
  return (result)
}

all.data <- analysis [
    ,
    read.repeat.data (file.name),
    by = .(
        file.name,
        sampling.time,
        delta.time,
        temperature.threshold,
        decision.tree
        )
]

data.to.plot <- all.data [
   ,
  .(success.rate = mean (success.rate)),
  by = .(
    criterion,
    max.depth,
    min.samples.split,
    delta.time,
    temperature.threshold
  )
]

make.plot <- function (
  data,
  label)
{
  cat ("\n* ** MAKE PLOT ** *\n")
  print (label)
  graphics <- ggplot (
    data = data,
    mapping = aes (
      x = delta.time,
      y = success.rate,
      color = factor (temperature.threshold)
    ))
  graphics <- graphics + geom_line () + geom_point ()
  graphics <- graphics + labs (
    x = "delta time (s)",
    y = "success rate",
    color = "temperature threshold (°C)"
    )
  graphics <- graphics + scale_y_continuous (
    labels = function (v) return (sprintf ("%.0f%%", v * 100)),
    limits = c (0.85, 1)
    )
  ggsave (
    filename = sprintf (
      "analysis-decision-tree_nature_%s.png",
      label
    ),
    plot = graphics,
    width = 8,
    height = 6,
    units = "in"
  )
  return (0)
}

data.to.plot [
   ,
    make.plot (.SD, sprintf ("%s_%d_%d", criterion, max.depth, min.samples.split)),
    by = .(criterion, max.depth, min.samples.split)
]
