library ("data.table")
library ("ggplot2")


analysis <- fread ("analysis.csv")

read.repeat.data <- function (
  filename
) {
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

data.to.plot <- analysis [
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

parameters <- list (
  list (
    variable = expression (success.rate),
    filename.suffix = "success-rate",
    label = "success rate"
  ),
  list (
    variable = expression (false.positive),
    filename.suffix = "false-positive",
    label = "false positive rate"
  ),
  list (
    variable = expression (false.negative),
    filename.suffix = "false-negative",
    label = "false negative rate"
  )
)

for (apar in parameters) {
    print (apar$label)
    graphics <- ggplot (
      data = data.to.plot,
      mapping = aes (
        x = decision.tree,
        y = eval (apar$variable)
      )
    ) + geom_boxplot (
    ) + facet_grid (
      delta.time ~ temperature.threshold
    ) + labs (
       x = "decision tree",
       y = apar$label
       )

    ggsave (
      filename = sprintf (
        "analysis-decision-tree_%s.png",
        apar$filename.suffix
      ),
      plot = graphics,
      width = 8,
      height = 6,
      units = "in"
    )
}

cat (sprintf (
    "The average random chance to win is %f.\nThe average score is %f.",
    data.to.plot [, mean (random.chance.winscore)],
    data.to.plot [, mean (success.rate)]
))
