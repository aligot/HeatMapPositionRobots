setwd("/home/aligot/Desktop/Arena/HeatmapPositionRobots/")

library(ggplot2)



data$Frame <- as.factor(data$Frame)

euc.dist <- function(x1, x2) sqrt(sum((x1 - x2) ^ 2))

midPointCircleDraw <- function(x, y, r) {
  points <- data.frame(X=integer(), 
                       Y=integer(),
                       stringsAsFactors = FALSE)
  dx <- r
  dy <- 0
  
  if (r > 0) {
    points <- rbind(points, c(x + r, y))
    points <- rbind(points, c(x,  y + r))
    points <- rbind(points, c(x - r, y))
    points <- rbind(points, c(x, y - r))
  }
  
  P <- 1-r
  
  while(dx > dy) {
    dy <- dy + 1
    
    if (P <= 0) {
      P <- P + 2*dy + 1;
    } else { 
      dx <- dx-1; 
      P <- P + 2*dy - 2*dx + 1; 
    } 
    
    if (dx < dy) {
      break
    }
    
    points <- rbind(points, c(dx + x, dy + y))
    points <- rbind(points, c(-dx + x, dy + y))
    points <- rbind(points, c(dx + x, -dy + y))
    points <- rbind(points, c(-dx + x, -dy + y))
    
    if (dx != dy) 
    { 
      points <- rbind(points, c(dy + x, dx + y))
      points <- rbind(points, c(-dy + x, dx + y))
      points <- rbind(points, c(dy + x, -dx + y))
      points <- rbind(points, c(-dy + x, -dx + y))
    } 
    
  }
  return(points)
}

fillInCircle <- function(circle_points) {
  colnames(circle_points) <- c('X', 'Y')
  points = circle_points[0,]
  Xs = unique(sort(circle_points$X))
  i <- 1
  for (x in Xs) {
    Ys = circle_points[which(circle_points$X==x),]$Y
    for (y in seq(min(Ys), max(Ys))) {
      points[i,] <- c(x, y)
      i <- i + 1
    }
  }
  return(points)
}


fromCentersToDisks <- function(data, outputname) {
  points <- data.frame(X=integer(), 
                       Y=integer(),
                       stringsAsFactors = FALSE) 
  r <- 15 # Rayon of the disk representing a robot
  for (i in 1:(nrow(data))) {
    print(paste(i, "/",nrow(data)))
    circlePoints <- midPointCircleDraw(data[i,]$X, data[i,]$Y, r)
    diskPoints <- fillInCircle(circlePoints)  
    #diskPoints <- circlePoints  
    colnames(diskPoints) <- c("X", "Y")
    points <- rbind(points, diskPoints)
  }
  
  write.csv(points, paste("ExtendedPoints/", outputname, ".csv", sep=''))
  return(points)
}


# Remove extra detected robots
refineData <- function(data) {
  data_refined <- data[0,]
  for (f in levels(data$Frame)) { # For each frame
    cur_dat = data[which(data$Frame==f),]
    #print(nrow(cur_dat))
    dist <- c()
    toBeRemoved <- c()
    for (i in (1:(nrow(cur_dat)-1))) {
      for (j in ((i+1):nrow(cur_dat))) {
        cur_dist <- euc.dist(c(cur_dat[i,]$X, cur_dat[i,]$Y), c(cur_dat[j,]$X, cur_dat[j,]$Y))
        dist <- c(dist, cur_dist)
        if (cur_dist < 30) {
          #print(paste("Distance", cur_dist))
          #print(cur_dat[i,])
          #print(cur_dat[j,])
          if (cur_dat[i,]$Radius >= cur_dat[j,]$Radius) {
            #print(paste("Delete",j))
            toBeRemoved <- c(toBeRemoved, j)
          } else {
            #print(paste("Delete",i))
            toBeRemoved <- c(toBeRemoved, i)
          }
        }
      }
    }
    if (length(toBeRemoved) > 0) {
      cur_dat = cur_dat[-toBeRemoved,]
    }
    data_refined <- rbind(data_refined, cur_dat)
  }
  
  return(data_refined)  
  
}


plotData <- function(points, outputname) {
  colnames(points) <- c('X','Y')
  ggplot(points, aes(x=X, y=Y)) +
    geom_bin2d(bins=1200) +
    xlim(0,1200) +
    ylim(1190,0) +
    scale_fill_continuous(type = "viridis") +
    #scale_y_reverse() +
    theme(
      panel.background = element_rect(fill = "transparent"), # bg of the panel
      plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
      panel.grid.major = element_blank(), # get rid of major grid
      panel.grid.minor = element_blank(), # get rid of minor grid
      legend.background = element_rect(fill = "transparent"), # get rid of legend bg
      legend.box.background = element_rect(fill = "transparent"), # get rid of legend panel bg
      axis.line=element_blank(),
      axis.text=element_blank(),
      axis.ticks=element_blank(),
      axis.title=element_blank(),
      panel.border=element_blank(),
      plot.margin= grid::unit(c(0, 0, 0, 0), "in"),
      legend.position="none"
    )
  ggsave(paste("Plots/", outputname, ".pdf", sep=''), plot=last_plot(), device = NULL, width = 45, height = 44, units = "cm", dpi = 200)
}




files <- list.files("Positions/", pattern ="\\.txt$")


########
# Main #
########
for (f in files) {
  data <- read.csv(paste("Positions/", f, sep=''), header = FALSE)
  
  colnames(data) <- c('Frame', 'X', 'Y', 'Radius')
  data$Frame <- as.factor(data$Frame)  
  
  refinedData <- refineData(data)
  
  outputname = strsplit(f, "\\.")[[1]][1]

  print(outputname)
  
  points <- fromCentersToDisks(refinedData, outputname)
  
  plotData(points, outputname)
}

      
      